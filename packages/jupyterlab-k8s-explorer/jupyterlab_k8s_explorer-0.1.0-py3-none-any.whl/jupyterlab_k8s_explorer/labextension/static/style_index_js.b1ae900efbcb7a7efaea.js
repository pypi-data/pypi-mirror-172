"use strict";
(self["webpackChunkjupyterlab_k8s_explorer"] = self["webpackChunkjupyterlab_k8s_explorer"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n/* Pen-specific styles */\nhtml,\nbody,\nsection {\n  height: 100%;\n}\n\n/* Pattern styles */\n.k8s-explorer-wrapper {\n  display: flex;\n}\n\n.menu {\n  background-color: #5a5a5a;\n  flex: 2;\n  padding: 1rem;\n  resize: horizontal;\n  float: left;\n}\n\n.content {\n  flex: 8;\n  padding: 1rem;\n  height: 90vh;\n  overflow-y: auto;\n}\n\n.cursor-pointer {\n  cursor: pointer;\n}\n\n.sub-menu-item {\n  font-size: 90%;\n}\n\n.menu-sidebar {\n  overflow-y: auto;\n  float: left;\n  width: 20vh;\n  height: 90vh;\n}\n\n.menu-item {\n  position: relative;\n  display: flex;\n  align-items: center;\n  width: 100%;\n  padding: 1rem 1.25rem;\n  font-size: 1rem;\n  text-align: left;\n  background-color: #e9e9e9;\n  border: 1;\n  border-radius: 1;\n  overflow-anchor: none;\n  background-repeat: no-repeat;\n  color: #1e1e1e;\n\n  --bs-btn-border-color: #fff;\n}\n\n.modal-fit-content {\n  width: 55rem;\n  max-width: none !important;\n}\n\n.table-content {\n  word-break: break-all;\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;;;;CAIC;;AAED,wBAAwB;AACxB;;;EAGE,YAAY;AACd;;AAEA,mBAAmB;AACnB;EACE,aAAa;AACf;;AAEA;EACE,yBAAyB;EACzB,OAAO;EACP,aAAa;EACb,kBAAkB;EAClB,WAAW;AACb;;AAEA;EACE,OAAO;EACP,aAAa;EACb,YAAY;EACZ,gBAAgB;AAClB;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,cAAc;AAChB;;AAEA;EACE,gBAAgB;EAChB,WAAW;EACX,WAAW;EACX,YAAY;AACd;;AAEA;EACE,kBAAkB;EAClB,aAAa;EACb,mBAAmB;EACnB,WAAW;EACX,qBAAqB;EACrB,eAAe;EACf,gBAAgB;EAChB,yBAAyB;EACzB,SAAS;EACT,gBAAgB;EAChB,qBAAqB;EACrB,4BAA4B;EAC5B,cAAc;;EAEd,2BAA2B;AAC7B;;AAEA;EACE,YAAY;EACZ,0BAA0B;AAC5B;;AAEA;EACE,qBAAqB;AACvB","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n/* Pen-specific styles */\nhtml,\nbody,\nsection {\n  height: 100%;\n}\n\n/* Pattern styles */\n.k8s-explorer-wrapper {\n  display: flex;\n}\n\n.menu {\n  background-color: #5a5a5a;\n  flex: 2;\n  padding: 1rem;\n  resize: horizontal;\n  float: left;\n}\n\n.content {\n  flex: 8;\n  padding: 1rem;\n  height: 90vh;\n  overflow-y: auto;\n}\n\n.cursor-pointer {\n  cursor: pointer;\n}\n\n.sub-menu-item {\n  font-size: 90%;\n}\n\n.menu-sidebar {\n  overflow-y: auto;\n  float: left;\n  width: 20vh;\n  height: 90vh;\n}\n\n.menu-item {\n  position: relative;\n  display: flex;\n  align-items: center;\n  width: 100%;\n  padding: 1rem 1.25rem;\n  font-size: 1rem;\n  text-align: left;\n  background-color: #e9e9e9;\n  border: 1;\n  border-radius: 1;\n  overflow-anchor: none;\n  background-repeat: no-repeat;\n  color: #1e1e1e;\n\n  --bs-btn-border-color: #fff;\n}\n\n.modal-fit-content {\n  width: 55rem;\n  max-width: none !important;\n}\n\n.table-content {\n  word-break: break-all;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base.css */ "./style/base.css");





/***/ })

}]);
//# sourceMappingURL=style_index_js.b1ae900efbcb7a7efaea.js.map