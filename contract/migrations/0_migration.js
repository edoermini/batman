var BAToken = artifacts.require("BAToken");
var MathLib = artifacts.require("Math");

module.exports = function(deployer) {
    // deployment steps
    deployer.deploy(MathLib);
    deployer.link(MathLib, BAToken);
    deployer.deploy(BAToken);
};