const fs = require('fs');
const path = require('path');

console.log('🔍 Verifying Blockchain & Privacy Integration...\n');

// Check if BlockchainPrivacy component exists
const blockchainComponentPath = path.join(__dirname, 'src/components/blockchain/BlockchainPrivacy.js');
const blockchainExists = fs.existsSync(blockchainComponentPath);

console.log(`✅ BlockchainPrivacy component exists: ${blockchainExists}`);

// Check App.js routing
const appPath = path.join(__dirname, 'src/App.js');
const appContent = fs.readFileSync(appPath, 'utf8');
const hasBlockchainImport = appContent.includes('import BlockchainPrivacy from');
const hasBlockchainRoute = appContent.includes('path="blockchain-privacy"');

console.log(`✅ App.js has BlockchainPrivacy import: ${hasBlockchainImport}`);
console.log(`✅ App.js has blockchain-privacy route: ${hasBlockchainRoute}`);

// Check Layout.js navigation
const layoutPath = path.join(__dirname, 'src/components/layout/Layout.js');
const layoutContent = fs.readFileSync(layoutPath, 'utf8');
const hasBlockchainNavItem = layoutContent.includes('Blockchain & Privacy');
const hasSecurityIcon = layoutContent.includes('Security as SecurityIcon');

console.log(`✅ Layout.js has Blockchain & Privacy nav item: ${hasBlockchainNavItem}`);
console.log(`✅ Layout.js has Security icon import: ${hasSecurityIcon}`);

// Check for old RealTimeAnalytics references
const hasOldAnalyticsImport = appContent.includes('import RealTimeAnalytics');
const hasOldAnalyticsRoute = appContent.includes('path="analytics"');
const hasOldAnalyticsNavItem = layoutContent.includes('Real-Time Analytics');

console.log(`\n🧹 Cleanup Status:`);
console.log(`❌ Old RealTimeAnalytics import removed: ${!hasOldAnalyticsImport}`);
console.log(`❌ Old analytics route removed: ${!hasOldAnalyticsRoute}`);
console.log(`❌ Old Analytics nav item removed: ${!hasOldAnalyticsNavItem}`);

console.log('\n🚀 Integration Summary:');
if (blockchainExists && hasBlockchainImport && hasBlockchainRoute && hasBlockchainNavItem && !hasOldAnalyticsImport && !hasOldAnalyticsRoute && !hasOldAnalyticsNavItem) {
  console.log('✅ All checks passed! Blockchain & Privacy integration is complete.');
} else {
  console.log('⚠️  Some issues found. Please check the details above.');
}
