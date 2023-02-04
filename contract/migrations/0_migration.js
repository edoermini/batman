var BAToken = artifacts.require("BAToken");
var MathLib = artifacts.require("Math");

var accounts = [ 
'0x772f437b0f15e1F205C8BD923b5C8357e9c0c429',
'0x5738d9100A6CB64FB78730746ab61472c7808fD9',
'0x7086D052EAaD359c7aCD9B993c6169aE0dEC0725',
'0x9fA18751b024FDC55cC85A484fF4261351Dd4666',
'0x95a29de4A8cc4697E627922d270Aa74C2bd7494a',
'0x332c22e9c7F02e092b18C6cc4D9Bfd46d36Dd7D9',
'0xaED2F48c0d06a13D1FE2853E7Ee3B7d0aA328d3B',
'0x88A0941f0dcb501C20b7BaE5a41608EB981f1209',
'0xad5d1cB78e80518b596A814340826F36B89660Fc',
'0x67E23e936C9d22eDCf9ebC9A989911b313c24BC1',
]

module.exports = function(deployer, network, accounts) {
    // deployment steps
    deployer.deploy(MathLib);
    deployer.link(MathLib, BAToken);
    deployer.deploy(BAToken, {"from":accounts[0]});
};