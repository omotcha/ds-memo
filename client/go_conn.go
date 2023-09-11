/*
Copyright (C) BABEC. All rights reserved.
Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.

SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"log"
	"math/big"
	"strings"

	"chainmaker.org/chainmaker/common/v2/evmutils/abi"
	"chainmaker.org/chainmaker/pb-go/v2/common"
	sdk "chainmaker.org/chainmaker/sdk-go/v2"
	"chainmaker.org/chainmaker/sdk-go/v2/examples"
)

const (
	createContractTimeout = 5
	contractName          = "memosolo001"
	version               = "1.0.0"
	byteCodePath          = "../../testdata/memosolo/MemoSolo.bin"
	abiPath               = "../../testdata/memosolo/MemoSolo.abi"

	configPath = "../sdk_configs/sdk_config_hsm.yml"
)

func main() {
	sdkTest(configPath)
}

func sdkTest(sdkPath string) {
	fmt.Println("====================== create client ======================")
	client, err := examples.CreateChainClientWithSDKConf(sdkPath)
	if err != nil {
		log.Fatalln(err)
	}

	fmt.Println("====================== create contract ======================")
	usernames := []string{examples.UserNameOrg1Admin1, examples.UserNameOrg2Admin1, examples.UserNameOrg3Admin1, examples.UserNameOrg4Admin1}
	testCreateContract(client, true, true, usernames...)

	fmt.Println("====================== 设置数值 ======================")
	testSet(client, 0, "about omotcha", "omotcha means toy in japanese", true, true)

	fmt.Println("====================== 查看数值 ======================")
	testGet(client, 0, true)

	//====================== 创建Storage合约 ======================
	//	CREATE EVM storage contract resp: message:"OK" contract_result:<result:"\n(b397dbecf8c200eced8441eff6504d712f61429b\022\0051.0.0\030\005*<\n\026wx-org1.chainmaker.org\020\001\032 $p^\215Q\366\236\2120\007\233eW\210\220\3746\250\027\331h\212\024\253\370Ecl\214J'\322" message:"OK" > tx_id:"4668c5dc91074119b96ad19f568ae06422488344c6224349bd71296b4fafea32"
	//====================== 设置数值 ======================
	//	invoke contract success, resp: [code:0]/[msg:OK]/[contractResult:gas_used:5375 ]
	//====================== 查看数值 ======================
	//val: [123]
}

func testCreateContract(client *sdk.ChainClient, withSyncResult bool, isIgnoreSameContract bool, usernames ...string) {

	codeBytes, err := ioutil.ReadFile(byteCodePath)
	if err != nil {
		log.Fatalln(err)
	}

	resp, err := createUserContract(client, contractName, version,
		string(codeBytes), common.RuntimeType_EVM, nil, withSyncResult, usernames...)
	if !isIgnoreSameContract {
		if err != nil {
			log.Fatalln(err)
		}
	}

	fmt.Printf("CREATE EVM storage contract resp: %+v\n", resp)
}

func createUserContract(client *sdk.ChainClient, contractName, version, byteCodePath string,
	runtime common.RuntimeType, kvs []*common.KeyValuePair, withSyncResult bool, usernames ...string) (*common.TxResponse, error) {

	payload, err := client.CreateContractCreatePayload(contractName, version, byteCodePath, runtime, kvs)
	if err != nil {
		return nil, err
	}

	endorsers, err := examples.GetEndorsers(payload, usernames...)
	//endorsers, err := examples.GetEndorsersWithAuthType(client.GetHashType(),
	//	client.GetAuthType(), payload, usernames...)
	if err != nil {
		return nil, err
	}

	resp, err := client.SendContractManageRequest(payload, endorsers, createContractTimeout, withSyncResult)
	if err != nil {
		return nil, err
	}

	err = examples.CheckProposalRequestResp(resp, true)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

func testSet(client *sdk.ChainClient, id int64, title string, content string, overwrite bool, withSyncResult bool) {
	abiJson, err := ioutil.ReadFile(abiPath)
	if err != nil {
		log.Fatalln(err)
	}

	myAbi, err := abi.JSON(strings.NewReader(string(abiJson)))
	if err != nil {
		log.Fatalln(err)
	}

	method := "writeMemo"
	dataByte, err := myAbi.Pack(method, big.NewInt(id), title, content, overwrite)
	if err != nil {
		log.Fatalln(err)
	}

	dataString := hex.EncodeToString(dataByte)

	kvs := []*common.KeyValuePair{
		{
			Key:   "data",
			Value: []byte(dataString),
		},
	}

	err = invokeUserContract(client, contractName, method, "", kvs, withSyncResult)
	if err != nil {
		log.Fatalln(err)
	}
}

func invokeUserContract(client *sdk.ChainClient, contractName, method, txId string, kvs []*common.KeyValuePair, withSyncResult bool) error {

	resp, err := client.InvokeContract(contractName, method, txId, kvs, -1, withSyncResult)
	if err != nil {
		return err
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return fmt.Errorf("invoke contract failed, [code:%d]/[msg:%s]\n", resp.Code, resp.Message)
	}

	if !withSyncResult {
		fmt.Printf("invoke contract success, resp: [code:%d]/[msg:%s]/[txId:%s]\n", resp.Code, resp.Message, resp.ContractResult.Result)
	} else {
		fmt.Printf("invoke contract success, resp: [code:%d]/[msg:%s]/[contractResult:%s]\n", resp.Code, resp.Message, resp.ContractResult)
	}

	return nil
}

func testGet(client *sdk.ChainClient, id int64, withSyncResult bool) {

	abiJson, err := ioutil.ReadFile(abiPath)
	if err != nil {
		log.Fatalln(err)
	}

	myAbi, err := abi.JSON(strings.NewReader(string(abiJson)))
	if err != nil {
		log.Fatalln(err)
	}

	method := "getMemoItemById"
	dataByte, err := myAbi.Pack(method, big.NewInt(id))
	if err != nil {
		log.Fatalln(err)
	}

	dataString := hex.EncodeToString(dataByte)

	kvs := []*common.KeyValuePair{
		{
			Key:   "data",
			Value: []byte(dataString),
		},
	}

	result, err := invokeUserContractWithResult(client, contractName, method, "", kvs, withSyncResult)
	if err != nil {
		log.Fatalln(err)
	}

	val, err := myAbi.Unpack("get", result)
	if err != nil {
		log.Fatalln(err)
	}
	fmt.Printf("val: %d\n", val)
}

func invokeUserContractWithResult(client *sdk.ChainClient, contractName, method, txId string,
	kvs []*common.KeyValuePair, withSyncResult bool) ([]byte, error) {

	resp, err := client.InvokeContract(contractName, method, txId, kvs, -1, withSyncResult)
	if err != nil {
		return nil, err
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return nil, fmt.Errorf("invoke contract failed, [code:%d]/[msg:%s]\n", resp.Code, resp.Message)
	}

	return resp.ContractResult.Result, nil
}
