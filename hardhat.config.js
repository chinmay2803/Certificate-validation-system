require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

/** @type import('hardhat/config').HardhatUserConfig */

module.exports = {
  solidity: "0.8.24", // or whatever version your contracts use
  networks: {
    hardhat: {},
    development: {
      url: "http://127.0.0.1:8545", // Localhost (Ganache or Hardhat Network)
    },
    sepolia: {
      url: `https://arbitrum-sepolia.infura.io/v3/${process.env.INFURA_PRIVATE_KEY}`,
      account: [`${process.env.PRIVATE_KEY}`],
    },
    // Add other networks as needed
  },
};