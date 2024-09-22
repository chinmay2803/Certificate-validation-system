// scripts/deploy.js

const hre = require("hardhat");
const fs = require('fs');

async function main() {
  console.log("Getting contract factory for Certification...");
  const Certification = await hre.ethers.getContractFactory("Certification");
  
  console.log("Deploying Certification contract...");
  const deployedCertification = await Certification.deploy();
  
  console.log("Waiting for deployment to be mined...");
  await deployedCertification.waitForDeployment();
  
  console.log(`Certification contract deployed at address: ${deployedCertification.target}`);
  
  const configData = {
    Certification: deployedCertification.target
  };
  
  fs.writeFileSync('./deployment_config.json', JSON.stringify(configData, null, 2));
  console.log("Deployment configuration saved to deployment_config.json");
}

// Execute the script
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Deployment failed:", error);
    process.exit(1);
  });
