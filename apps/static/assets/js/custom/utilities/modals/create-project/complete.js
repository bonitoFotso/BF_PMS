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

/***/ "../demo41/src/js/custom/utilities/modals/create-project/complete.js":
/*!***************************************************************************!*\
  !*** ../demo41/src/js/custom/utilities/modals/create-project/complete.js ***!
  \***************************************************************************/
/***/ ((module) => {

eval("\n\n// Class definition\nvar KTModalCreateProjectComplete = function () {\n\t// Variables\n\tvar startButton;\n\tvar form;\n\tvar stepper;\n\n\t// Private functions\n\tvar handleForm = function() {\n\t\tstartButton.addEventListener('click', function () {\n\t\t\tstepper.goTo(1);\n\t\t});\n\t}\n\n\treturn {\n\t\t// Public functions\n\t\tinit: function () {\n\t\t\tform = KTModalCreateProject.getForm();\n\t\t\tstepper = KTModalCreateProject.getStepperObj();\n\t\t\tstartButton = KTModalCreateProject.getStepper().querySelector('[data-kt-element=\"complete-start\"]');\n\n\t\t\thandleForm();\n\t\t}\n\t};\n}();\n\n// Webpack support\nif ( true && typeof module.exports !== 'undefined') {\n\twindow.KTModalCreateProjectComplete = module.exports = KTModalCreateProjectComplete;\n}\n\n\n//# sourceURL=webpack://metronic/../demo41/src/js/custom/utilities/modals/create-project/complete.js?");

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
/******/ 	var __webpack_exports__ = __webpack_require__("../demo41/src/js/custom/utilities/modals/create-project/complete.js");
/******/ 	
/******/ })()
;