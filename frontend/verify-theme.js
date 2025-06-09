// Theme verification script
const { lightTheme, darkTheme } = require('./src/theme/index.js');

console.log('🎨 Theme Verification Test');
console.log('==========================');

// Test light theme
console.log('\n✅ Light Theme:');
console.log('- Type:', typeof lightTheme);
console.log('- Has $$material:', lightTheme.$$material ? 'Yes' : 'No');
console.log('- Primary color:', lightTheme.palette?.primary?.main);
console.log('- Background:', lightTheme.palette?.background?.default);

// Test dark theme
console.log('\n✅ Dark Theme:');
console.log('- Type:', typeof darkTheme);
console.log('- Has $$material:', darkTheme.$$material ? 'Yes' : 'No');
console.log('- Primary color:', darkTheme.palette?.primary?.main);
console.log('- Background:', darkTheme.palette?.background?.default);

// Test if themes are valid Material-UI theme objects
console.log('\n🧪 Theme Structure Validation:');
console.log('- Light theme has palette:', !!lightTheme.palette);
console.log('- Light theme has typography:', !!lightTheme.typography);
console.log('- Light theme has components:', !!lightTheme.components);
console.log('- Dark theme has palette:', !!darkTheme.palette);
console.log('- Dark theme has typography:', !!darkTheme.typography);
console.log('- Dark theme has components:', !!darkTheme.components);

console.log('\n🎉 Theme verification complete!');
