// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.4;

contract MemoSolo {

    // version
    string public constant VERSION = "0.0.1";

    // memo for soloer: admin is contract creator
    address private admin;

    constructor() {
        admin = msg.sender;
    }

    // memo item data structure
    struct MemoItem {
        uint256 updateTime;
        string title;
        string content;
    }

    // storages
    string[] private _titles;
    mapping(string=>MemoItem) private _memos;

    ////////////////
    //   events   //
    ////////////////

    event MemoUpdated(string title, string content);

    ///////////////////
    //   modifiers   //
    ///////////////////
    modifier onlyOwner() {
        require(msg.sender == admin, "only admin has access");
        _;
    }

    modifier memoExists(string memory title) {
        require(_memos[title].updateTime > 0, "memo not found");
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
    function writeMemo(string memory title, string memory content, bool overwrite) public onlyOwner {
        if(!overwrite){
            require(_memos[title].updateTime == 0, "memo already exists");
        }
        if(_memos[title].updateTime == 0){
            _titles.push(title);
        }
        _memos[title].updateTime = block.timestamp;
        _memos[title].title = title;
        _memos[title].content = content;
        emit MemoUpdated(title, content);
    }


    /////////////////
    //   getters   //
    /////////////////
    function getTitles() public view onlyOwner returns (string[] memory){
        return _titles;
    }

    function getMemoItemByTitle(string memory title) 
    public view onlyOwner memoExists(title) 
    returns (uint256 _updateTime, string memory _content){
        _updateTime = _memos[title].updateTime;
        _content = _memos[title].content;
    }
}