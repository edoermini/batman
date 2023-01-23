// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract BAToken { 
    uint public constant PRICE = 2 * 1e15;
    uint public verifyCost;
    mapping(address => uint) public balance;
    
    address payable minter;
    uint totalAddresses;
    uint totalBalance;

    enum ExploitType {
        DOS,
        Local,
        Remote,
        Webapp
    }

    mapping(string => ExploitType) stringToExploitType;

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
        address[] verifiers;
        uint[] tokens;
        mapping(address => bool) hasVerified;
    }

    PoC[] public pocs;

    constructor() {
        minter = payable(msg.sender);// qua ci va il cast (payable) per rendere msg.sender payable che non lo è 
        totalAddresses = 0;
        totalBalance = 0;
        verifyCost = 10;
        stringToExploitType["DOS"] = ExploitType.DOS;
        stringToExploitType["Local"] = ExploitType.Local;
        stringToExploitType["Remote"] = ExploitType.Remote;
        stringToExploitType["Webapp"] = ExploitType.Webapp;
    }

    function mint() public payable {
        require(msg.value >= PRICE, "Not enough value for a token");
        
        uint tokens = msg.value / PRICE;

        if (balance[msg.sender] == 0) {
            totalAddresses += 1;
        }
       
        balance[msg.sender] += tokens;
        uint intialBalance = totalBalance;
        totalBalance += tokens;

        updateVerifyCost(intialBalance);
    }

    /*
    In order to verify verifiers must stake a number of tokens defined by verifyCost
    Once the majority of voters is reached for a certain PoC the author gains the 20% of the tota tokens staked
    and the voters gain a percentage proportional to the number of voters.
    */
    function verify(uint pocID) public {
        require((pocID >= 0 && pocID < pocs.length), "This PoC doesn't exist");
        require(pocs[pocID].verified == false, "PoC already verified");
        require(balance[msg.sender] >= verifyCost, "Not enough tokens for verify");
        require(pocs[pocID].hasVerified[msg.sender] == false, "You already verified this PoC");
        
        pocs[pocID].hasVerified[msg.sender] = true;
        pocs[pocID].verifiers.push(msg.sender);
        pocs[pocID].tokens.push(verifyCost);
        
        balance[msg.sender] -= verifyCost;

        if (pocs[pocID].verifiers.length < (totalAddresses/2)+1) {
            return;
        }

        // majority reached

        pocs[pocID].verified = true;
        uint initialBalance = totalBalance;

        uint totalStaked = 0;

        for (uint i=0; i < pocs[pocID].tokens.length; i++) {
            totalStaked += pocs[pocID].tokens[i];
        }
        
        uint authorGain = (totalStaked*20)/100;
        if ((totalStaked*20)%100 > 0) {
            authorGain += 1;
        }

        balance[pocs[pocID].author] += authorGain;
        totalBalance += authorGain;

        for (uint i=0; i < pocs[pocID].verifiers.length; i++) {
            uint gain = pocs[pocID].tokens[i]*pocs[pocID].tokens[i] / totalStaked;

            if (pocs[pocID].tokens[i]*pocs[pocID].tokens[i] % totalStaked > 0) {
                gain += 1;
            }

            balance[pocs[pocID].verifiers[i]] += verifyCost + gain;
            totalBalance += gain;
        }

        updateVerifyCost(initialBalance);
    }

    function updateVerifyCost(uint initialBalance) private {
        // verify cost increase proportionally to the gain of the author and verifiers
        // verifyCost = verifyCost + verifyCost*((totalBalance/initialBalance) - 1)

        uint x = totalBalance * verifyCost;
        uint y = x / initialBalance;

        if (x % initialBalance > 0) {
            y += 1;
        }

        uint verifyCostIncrease = y - verifyCost;

        verifyCost += verifyCostIncrease;
    }

    // function publish(string poc, uint severity, string cve, string exploit, string title, string tag)
    // function read(pocID)
    // function readAll()
    // function readAll(address author, string exploit, bool verified, uint severity)

    function withdraw(uint amount) public {
        require(msg.sender == minter, "You cannot withdraw");
        payable(msg.sender).transfer(amount);
    }

    function terminate() public {
        require(msg.sender == minter, "You can't terminate the contract");
        selfdestruct(minter);
    }

    
}