const hre = require("hardhat");

async function main() {
  const Certification = await hre.ethers.getContractFactory("Certification");
  const deployedCertification = await Certification.deploy();
  
  await deployedCertification.deployed();
  
  console.log(`Certification contract deployed at address: ${deployedCertification.address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
