/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "../demo41/src/js/custom/landing.js":
/*!******************************************!*\
  !*** ../demo41/src/js/custom/landing.js ***!
  \******************************************/
/***/ ((module) => {

eval("\n\n// Class definition\nvar KTLandingPage = function () {\n    // Private methods\n    var initTyped = function() {\n        var typed = new Typed(\"#kt_landing_hero_text\", {\n            strings: [\"The Best Theme Ever\", \"The Most Trusted Theme\", \"#1 Selling Theme\"],\n            typeSpeed: 50\n        });\n    }\n\n    // Public methods\n    return {\n        init: function () {\n            //initTyped();\n        }   \n    }\n}();\n\n// Webpack support\nif (true) {\n    module.exports = KTLandingPage;\n}\n\n// On document ready\nKTUtil.onDOMContentLoaded(function() {\n    KTLandingPage.init();\n});\n\n\n//# sourceURL=webpack://metronic/../demo41/src/js/custom/landing.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("../demo41/src/js/custom/landing.js");
/******/ 	
/******/ })()
;