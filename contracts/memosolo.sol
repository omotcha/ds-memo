// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.4;

contract MemoSolo {

    // version
    string public constant VERSION = "0.0.3";

    // memo for soloer: admin is contract creator and only user
    address private admin;

    constructor() {
        admin = msg.sender;
    }

    // memo item data structure
    struct MemoItem {
        uint256 updateTime;
        uint256 id;
        string title;
        string content;
    }

    // storages
    uint256[] private _ids;
    mapping(uint256=>MemoItem) private _memos;

    ////////////////
    //   events   //
    ////////////////

    event MemoUpdated(uint256 id, string title, string content);

    ///////////////////
    //   modifiers   //
    ///////////////////
    modifier onlyOwner() {
        require(msg.sender == admin, "only admin has access");
        _;
    }

    modifier memoExists(uint256 id) {
        require(_memos[id].updateTime > 0, "memo not found");
        _;
    }

    ////////////////////////////
    //   external functions   //
    ////////////////////////////

    /**
     * update a memo item
     * @param title memo title
     * @param content memo content
     * @param overwrite if do overwrite
     */
    function writeMemo(uint256 id, string memory title, string memory content, bool overwrite) public onlyOwner {
        if(!overwrite){
            require(_memos[id].updateTime == 0, "memo already exists");
        }
        if(_memos[id].updateTime == 0){
            _ids.push(id);
        }
        _memos[id].updateTime = block.timestamp;
        _memos[id].id = id;
        _memos[id].title = title;
        _memos[id].content = content;
        emit MemoUpdated(id, title, content);
    }


    /////////////////
    //   getters   //
    /////////////////
    function getIds() public view onlyOwner returns (uint256[] memory){
        return _ids;
    }

    function getMemoItemById(uint256 id) 
    public view onlyOwner memoExists(id) 
    returns (uint256 _updateTime, string memory _title, string memory _content){
        _updateTime = _memos[id].updateTime;
        _title = _memos[id].title;
        _content = _memos[id].content;
    }

    function getAllTitlesWithIds() public view onlyOwner returns (string[] memory titles, uint256[] memory ids){
        uint256 i;
        uint256 len = _ids.length;
        titles = new string[](len);
        for(i=0;i<len;i++){
            titles[i] = _memos[i].title;
        }
        ids = _ids;
    }
}