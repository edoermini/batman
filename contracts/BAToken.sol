// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract BAToken {
    address public minter;
    mapping(address => uint) public balance;
    uint public constant PRICE = 2 * 1e15;

    enum ExploitType {
        DOS,
        Local,
        Remote,
        Webapp
    }

    mapping(string => ExploitType) private stringToExploitType;

    struct PoC {
        uint pocID;
        address author;
        string poc;
        string pocHash;
        uint severity;
        string cve;
        ExploitType exploit;
        string title;
        bool verified;
        mapping(address => uint) verifiers;
    }

    PoC[] PoCs;

    constructor() {
        minter = msg.sender;
        stringToExploitType["DOS"] = ExploitType.DOS;
        stringToExploitType["Local"] = ExploitType.Local;
        stringToExploitType["Remote"] = ExploitType.Remote;
        stringToExploitType["Webapp"] = ExploitType.Webapp;
    }

    function mint() public payable {
        require(msg.value >= PRICE, "Not enough value for a token");
        balance[msg.sender] += msg.value / PRICE;
    }

    function verify(uint pocID, uint tokens) public {
        /*
        People must put a minimun number of token that is incremented once a PoC is verified
        The gain for the author is 20% of the total token staked.
        The gain for the voters is the total tokens staked by the voter + the percentage of the tokens staked
        */
    }

    // function publish(string poc, uint severity, string cve, string exploit, string title, string tag)
    // function read(pocID)
    // function readAll()
    // function readAll(address author, string exploit, bool verified, uint severity)

    function terminate() public {
        require(msg.sender == minter, "You can't terminate the contract");
        selfdestruct(payable(minter));
    }

    
}