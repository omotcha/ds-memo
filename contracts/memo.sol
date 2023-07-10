// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.4;

contract Memo {

    // version
    string public constant VERSION = "0.0.1";

    // memo for public: admin is contract creator
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
    mapping(address=>uint256[]) _ids;
    mapping(address=>mapping(uint256=>MemoItem)) private _memos;

    ////////////////
    //   events   //
    ////////////////

    event MemoUpdated(address user, uint256 id, string title, string content);

    ///////////////////
    //   modifiers   //
    ///////////////////
    modifier onlyAdmin() {
        require(msg.sender == admin, "only admin has access");
        _;
    }


    modifier memoExists(uint256 id) {
        require(_memos[msg.sender][id].updateTime > 0, "memo not found");
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
    function writeMemo(uint256 id, string memory title, string memory content, bool overwrite) public {
        if(!overwrite){
            require(_memos[msg.sender][id].updateTime == 0, "memo already exists");
        }
        if(_memos[msg.sender][id].updateTime == 0){
            _ids[msg.sender].push(id);
        }
        _memos[msg.sender][id].updateTime = block.timestamp;
        _memos[msg.sender][id].id = id;
        _memos[msg.sender][id].title = title;
        _memos[msg.sender][id].content = content;
        emit MemoUpdated(msg.sender, id, title, content);
    }


    /////////////////
    //   getters   //
    /////////////////
    function getIds() public view returns (uint256[] memory){
        return _ids[msg.sender];
    }

    function getMemoItemById(uint256 id) 
    public view memoExists(id) 
    returns (uint256 _updateTime, string memory _title, string memory _content){
        _updateTime = _memos[msg.sender][id].updateTime;
        _title = _memos[msg.sender][id].title;
        _content = _memos[msg.sender][id].content;
    }

    function getAllTitlesWithIds() public view returns (string[] memory titles, uint256[] memory ids){
        uint256 i;
        uint256 len = _ids[msg.sender].length;
        titles = new string[](len);
        for(i=0;i<len;i++){
            titles[i] = _memos[msg.sender][i].title;
        }
        ids = _ids[msg.sender];
    }
}