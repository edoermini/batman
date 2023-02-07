// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

library Math {
    function ceilDivision(uint dividend, uint divisor) internal pure returns (uint ceiledQuotient) {
        ceiledQuotient = dividend/divisor;
        
        if (dividend%divisor > 0) {
            ceiledQuotient += 1;
        }

        return ceiledQuotient;
    }
}

/*
* @notice   The contract allows to publish cve's Proof of Concepts (PoC) and to verify them using a majority based voting system.
*           Every time a verification for a certain PoC is asked the verifier spends a certain amount of tokens.
*           This amount is increased every time the total balance of the tokens increases accordingly.
*           Once a PoCs verification is asked from a majority of voter the PoC is flagged as verified and each voter and the PoC's author gain tokens
*/
contract BAToken { 
    uint public constant PRICE = 2 * 1e15;

    uint public verifyCost;
    mapping(address => uint) public balance;
    
    address payable minter;

    uint totalAddresses;
    uint totalBalance;

    mapping(string => bool) exploitTypes;

    struct PoC {
        uint pocID;
        address author;
        string poc;
        string language;
        bytes32 pocHash;
        uint severity;
        string cve;
        string exploitType;
        string title;
        bool verified;
        address[] verifiers;
        uint[] tokens;
    }

    PoC[] public pocs;

    event Minted(uint tokens, uint newBalance);
    event Verified(uint pocID, address author, string title);
    event Published(uint pocID);

    constructor() {
        minter = payable(msg.sender);
        totalAddresses = 0;
        totalBalance = 0;
        verifyCost = 10;
        exploitTypes["DOS"] = true;
        exploitTypes["Local"] = true;
        exploitTypes["Remote"] = true;
        exploitTypes["Webapp"] = true;
    }

    /*
    * @notice   Adds tokens to the sender's balance according to the given value 
    * @dev      Updates the balance with the new tokens and updates the verify cost accordingly to the number of new tokens
    */
    function mint() public payable {
        require(msg.value >= PRICE, "Not enough value for a token");
        
        uint tokens = msg.value / PRICE;

        if (balance[msg.sender] == 0) {
            totalAddresses += 1;
        }
       
        balance[msg.sender] += tokens;
        totalBalance += tokens;

        emit Minted(tokens, balance[msg.sender]);
    }

    /*
    * @notice   Stores the verify request to the given PoC. 
    *           Once the majority is reached each verifier gains a percentage according to the amount of tokens spent to request the verification
    *           and the PoC author gains the 20% of the total tokens spent.
    *           Once a PoC is verified the verify cost increases according to the number of tokens generated.
    * @params pocID The ID of the proof of concept to verify 
    */
    function verify(uint pocID) public {
        require((pocID >= 0 && pocID < pocs.length), "This PoC doesn't exist");
        require((msg.sender != pocs[pocID].author), "You cannot verify your PoCs");
        require(pocs[pocID].verified == false, "PoC already verified");
        require(balance[msg.sender] >= verifyCost, "Not enough tokens for verify");
        require(hasVerified(pocID, msg.sender) == false, "You already verified this PoC");
        
        // stores the verifier
        pocs[pocID].verifiers.push(msg.sender);

        // stores the amount of tokens that verifier spent
        pocs[pocID].tokens.push(verifyCost);
        
        balance[msg.sender] -= verifyCost;

        if (pocs[pocID].verifiers.length <= ((totalAddresses-1)/2)) {
            // majority not reached yet
            return;
        }

        // majority reached

        // flags the PoC as verified
        pocs[pocID].verified = true;

        // stores the balance before generating new tokens
        uint initialBalance = totalBalance;
        
        // computing the author gain (20% of the total tokens spent to verify)
        uint totalStaked = 0;
        for (uint i=0; i < pocs[pocID].tokens.length; i++) {
            totalStaked += pocs[pocID].tokens[i];
        }
        uint authorGain = Math.ceilDivision(totalStaked*20, 100);

        // updating the balance
        balance[pocs[pocID].author] += authorGain;
        totalBalance += authorGain;
        
        // computing the gain of the verifiers and updating the balance
        for (uint i=0; i < pocs[pocID].verifiers.length; i++) {
            uint gain = Math.ceilDivision(pocs[pocID].tokens[i]*pocs[pocID].tokens[i], totalStaked);
            
            balance[pocs[pocID].verifiers[i]] += verifyCost + gain;
            totalBalance += gain;
        }

        emit Verified(pocID, pocs[pocID].author, pocs[pocID].title);
       
        updateVerifyCost(initialBalance);
    }

    /*
    * @notice Publishes a poc
    * @param _poc The poc's code
    * @param _cve The poc's cve
    * @param _exploit The type of exploit
    * @param _title The poc's title
    */
    function publish(string memory _poc, uint _severity, string memory _cve, string memory _type, string memory _title, string memory _language) public {
        require(exploitTypes[_type] == true, "_exploit must be one among: Remote, Local, DOS or Webapp");

        // computes the poc's code hash
        bytes32 _pocHash = keccak256(bytes(_poc));

        require(checkPoCExistence(_pocHash) == false, "This PoC already exists");

        address[] memory _verifiers;
        uint[] memory _tokens;
        uint _pocID = pocs.length;

        // creates the new PoC entry
        PoC memory newPoC = PoC(
            {
                pocID: _pocID,
                author: msg.sender,
                poc: _poc,
                language: _language,
                pocHash: _pocHash,
                severity: _severity,
                cve: _cve,
                exploitType: _type,
                title: _title,
                verified: false,
                verifiers: _verifiers,
                tokens: _tokens
            }
        );

        // adds the poc in the list
        pocs.push(newPoC);

        emit Published(_pocID);
    }

    /*
    * @notice Reads all published proof of concepts
    * @return PoC[] The published PoCs
    */
    function readAll() public view returns (PoC[] memory) {
        return pocs;
    }

    /*
    * @notice Terminates the contract
    */
    function terminate() public {
        require(msg.sender == minter, "You can't terminate the contract");
        selfdestruct(minter);
    }

    /*
    * @notice Transfers tokens from an account to another
    * @param from The donator from which tokes are taken
    * @param to The recipient of the donation
    * @param amount The amount of tokens to transfer
    */
    function donate(address recipient, uint amount) public {
        require(msg.sender != recipient, "You can't make a donation to yourself");
        require(balance[msg.sender] >= amount, "You don't have enough tokens");

        balance[msg.sender] -= amount;
        balance[recipient] += amount;
    }
    
    /*
    * @notice Updates the verify cost accordingly to the increase of the total balance
    * @dev The function is called every time the total balance increases and the increase of the verify cost is proportional to the increase of the total balance
    * @param initialBalance The balance's value before the increase
    */
    function updateVerifyCost(uint initialBalance) private {
        // verifyCost = verifyCost + verifyCost*((totalBalance/initialBalance) - 1)

        if (initialBalance == 0) {
            return;
        }

        uint x = totalBalance * verifyCost;
        uint y = Math.ceilDivision(x, initialBalance);

        uint verifyCostIncrease = y - verifyCost;

        verifyCost += verifyCostIncrease;
    }

    /*
    * @notice Checks if a poc already exists using the code's hash
    * @param pocHash the code's hash
    * @return bool True if the PoC exists, False otherwise
    */
    function checkPoCExistence(bytes32 pocHash) private view returns (bool) {

        for (uint i = 0; i < pocs.length; i++) {
            if (pocs[i].pocHash == pocHash) {
                return true;
            }
        }

        return false;
    }

    /*
    * @notice Checks if a verifier has already verified a PoC
    * @param pocID The PoC's ID
    * @param verifier The verifier address
    * @return bool True if the varifier has already verified, False otherwise
    */
    function hasVerified(uint pocID, address verifier) private view returns (bool) {
        for (uint i = 0; i < pocs[pocID].verifiers.length; i++) {
            if (pocs[pocID].verifiers[i] == verifier) {
                return true;
            }
        }

        return false;
    }

}
