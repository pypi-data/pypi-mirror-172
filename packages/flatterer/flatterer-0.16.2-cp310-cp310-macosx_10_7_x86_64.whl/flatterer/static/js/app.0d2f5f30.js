(function(e){function t(t){for(var s,o,r=t[0],l=t[1],c=t[2],u=0,p=[];u<r.length;u++)o=r[u],Object.prototype.hasOwnProperty.call(n,o)&&n[o]&&p.push(n[o][0]),n[o]=0;for(s in l)Object.prototype.hasOwnProperty.call(l,s)&&(e[s]=l[s]);d&&d(t);while(p.length)p.shift()();return i.push.apply(i,c||[]),a()}function a(){for(var e,t=0;t<i.length;t++){for(var a=i[t],s=!0,o=1;o<a.length;o++){var l=a[o];0!==n[l]&&(s=!1)}s&&(i.splice(t--,1),e=r(r.s=a[0]))}return e}var s={},n={app:0},i=[];function o(e){return r.p+"js/"+({about:"about"}[e]||e)+"."+{about:"81ef6e5f"}[e]+".js"}function r(t){if(s[t])return s[t].exports;var a=s[t]={i:t,l:!1,exports:{}};return e[t].call(a.exports,a,a.exports,r),a.l=!0,a.exports}r.e=function(e){var t=[],a=n[e];if(0!==a)if(a)t.push(a[2]);else{var s=new Promise((function(t,s){a=n[e]=[t,s]}));t.push(a[2]=s);var i,l=document.createElement("script");l.charset="utf-8",l.timeout=120,r.nc&&l.setAttribute("nonce",r.nc),l.src=o(e);var c=new Error;i=function(t){l.onerror=l.onload=null,clearTimeout(u);var a=n[e];if(0!==a){if(a){var s=t&&("load"===t.type?"missing":t.type),i=t&&t.target&&t.target.src;c.message="Loading chunk "+e+" failed.\n("+s+": "+i+")",c.name="ChunkLoadError",c.type=s,c.request=i,a[1](c)}n[e]=void 0}};var u=setTimeout((function(){i({type:"timeout",target:l})}),12e4);l.onerror=l.onload=i,document.head.appendChild(l)}return Promise.all(t)},r.m=e,r.c=s,r.d=function(e,t,a){r.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},r.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},r.t=function(e,t){if(1&t&&(e=r(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(r.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var s in e)r.d(a,s,function(t){return e[t]}.bind(null,s));return a},r.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="/",r.oe=function(e){throw console.error(e),e};var l=window["webpackJsonp"]=window["webpackJsonp"]||[],c=l.push.bind(l);l.push=t,l=l.slice();for(var u=0;u<l.length;u++)t(l[u]);var d=c;i.push([0,"chunk-vendors"]),a()})({0:function(e,t,a){e.exports=a("56d7")},"56d7":function(e,t,a){"use strict";a.r(t);a("e260"),a("e6cf"),a("cca6"),a("a79d");var s=a("2b0e"),n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-app",[a("v-navigation-drawer",{attrs:{app:"",width:"350"}},[a("v-list-item",{attrs:{to:"/"}},[a("v-list-item-content",[a("img",{staticStyle:{flex:"none"},attrs:{width:"150",src:"https://raw.githubusercontent.com/kindly/flatterer/main/docs/_static/flatterer-with-inline-text.svg"}})])],1),a("v-divider"),a("v-list-item",{attrs:{to:"about"}},[a("v-list-item-content",[a("v-list-item-title",{staticClass:"subtitle-1"},[e._v(" About ")])],1)],1),a("v-divider"),a("v-list",{attrs:{dense:"",nav:""},model:{value:e.listItem,callback:function(t){e.listItem=t},expression:"listItem"}},["Home"==e.$route.name?a("v-list-item-group",{model:{value:e.listItem,callback:function(t){e.listItem=t},expression:"listItem"}},[a("v-list-item",{attrs:{dense:"",href:"#json-input",value:"json-input"}},[e._v(" JSON Input ")]),a("v-list-item",{attrs:{dense:"",href:"#options",value:"options"}},[e._v(" Options ")]),e.sections.error?a("v-list-item",{attrs:{dense:"",href:"#error",value:"error"}},[e._v("Error")]):e._e(),e.sections.error?a("v-list-item",{attrs:{dense:"",href:"#input-data-preview",value:"input-data-preview"}},[e._v("Input Data Preview")]):e._e(),e.sections.tables?a("v-list-item",{attrs:{dense:"",href:"#tables-preview",value:"tables-preview"}},[e._v("Tables")]):e._e(),e._l(e.sections.tables,(function(t){return a("v-list-item",{key:t,staticClass:"body-2 pl-10",staticStyle:{"min-height":"10px"},attrs:{dense:"",value:"table-"+t,href:"#table-"+t}},[e._v(e._s(t))])})),e.sections.tables?a("v-list-item",{attrs:{dense:"",href:"#download",value:"download"}},[e._v("Table Downloads")]):e._e()],2):e._e()],1)],1),a("v-main",[a("router-view")],1)],1)},i=[],o={name:"App",computed:{sections:function(){return this.$store.state.sections},listItem:{get:function(){return this.$store.state.listItem},set:function(e){this.$store.commit("setListItem",e)}}},data:function(){return{}}},r=o,l=a("2877"),c=a("6544"),u=a.n(c),d=a("7496"),p=a("ce7e"),v=a("8860"),f=a("da13"),h=a("5d23"),m=a("1baa"),b=a("f6c4"),_=a("f774"),w=Object(l["a"])(r,n,i,!1,null,null,null),y=w.exports;u()(w,{VApp:d["a"],VDivider:p["a"],VList:v["a"],VListItem:f["a"],VListItemContent:h["a"],VListItemGroup:m["a"],VListItemTitle:h["b"],VMain:b["a"],VNavigationDrawer:_["a"]});a("d3b7"),a("3ca3"),a("ddb0");var x=a("8c4f"),g=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-container",[a("v-card",[a("v-row",[a("v-col",[a("v-card-title",{directives:[{name:"intersect",rawName:"v-intersect",value:e.onIntersect,expression:"onIntersect"}],attrs:{id:"json-input"}},[e._v("JSON Input")])],1),a("v-col",[a("v-container",[a("v-btn",{staticClass:"float-right",attrs:{color:"deep-orange lighten-4",disabled:"new"===e.formState},on:{click:e.reset}},[e._v("reset all")])],1)],1)],1),a("v-container",[a("v-expansion-panels",{model:{value:e.panel,callback:function(t){e.panel=t},expression:"panel"}},[a("v-expansion-panel",[a("v-expansion-panel-header",[e._v("Upload File")]),a("v-expansion-panel-content",[a("v-file-input",{attrs:{label:"File input",id:"file-input",name:"file",outlined:"",dense:"",required:""},model:{value:e.fileUpload,callback:function(t){e.fileUpload=t},expression:"fileUpload"}})],1)],1),a("v-expansion-panel",[a("v-expansion-panel-header",[e._v("Download from URL")]),a("v-expansion-panel-content",[a("v-text-field",{attrs:{outlined:"",label:"URL of JSON file",dense:"",placeholder:"https://link/to/file.json"},model:{value:e.url,callback:function(t){e.url=t},expression:"url"}})],1)],1),a("v-expansion-panel",[a("v-expansion-panel-header",[e._v("Paste")]),a("v-expansion-panel-content",[a("v-textarea",{attrs:{outlined:"",label:"JSON data"},model:{value:e.paste,callback:function(t){e.paste=t},expression:"paste"}})],1)],1)],1)],1),a("v-container",[a("v-card",[a("v-container",[a("v-row",[a("v-col",[a("h3",{directives:[{name:"intersect",rawName:"v-intersect",value:e.onIntersect,expression:"onIntersect"}],attrs:{id:"options"}},[e._v("Options")])])],1),a("v-row",{staticClass:"mt-0"},[a("v-col",[a("v-radio-group",{staticClass:"mt-0",attrs:{row:"",mandatory:"",dense:"",messages:"Position where main data array exists."},scopedSlots:e._u([{key:"label",fn:function(){return[a("strong",[e._v("Position in JSON:")])]},proxy:!0}]),model:{value:e.arrayPosition,callback:function(t){e.arrayPosition=t},expression:"arrayPosition"}},[a("v-radio",{attrs:{label:"Guess based on data",value:"top"}}),a("v-radio",{attrs:{label:"JSON stream",value:"stream"}}),a("v-radio",{attrs:{label:"Array in object",value:"nested"}})],1)],1),a("v-col",[a("v-text-field",{style:{visibility:"nested"==e.arrayPosition?"visible":"hidden"},attrs:{outlined:"",dense:"",label:"Key in object of data array",messages:"The key in the object where the main array of objects exists."},model:{value:e.array_key,callback:function(t){e.array_key=t},expression:"array_key"}})],1)],1),a("v-row",[a("v-col",[a("v-text-field",{attrs:{outlined:"",dense:"",messages:"Table name that represents main data array in input.  Defaults to `main`.",label:"Main Table Name",placeholder:"main"},model:{value:e.main_table_name,callback:function(t){e.main_table_name=t},expression:"main_table_name"}})],1),a("v-col",[a("v-checkbox",{attrs:{outlined:"",dense:"","hide-details":"true",label:"Inline arrays with only single item"},model:{value:e.inline_one_to_one,callback:function(t){e.inline_one_to_one=t},expression:"inline_one_to_one"}})],1)],1),a("v-row",[a("v-col",[a("v-text-field",{attrs:{outlined:"",dense:"",label:"JSONSchema URL",placeholder:"https://path/to/schema",messages:"URL where JSONSchema representing a single item in data array exists. If empty do not use schema"},model:{value:e.json_schema,callback:function(t){e.json_schema=t},expression:"json_schema"}})],1),a("v-col",[a("v-select",{style:{visibility:e.json_schema.startsWith("http")?"visible":"hidden"},attrs:{items:e.useTitle,dense:"",label:"Use titles from schema",messages:"Options for using titles within schema"},model:{value:e.schemaTitle,callback:function(t){e.schemaTitle=t},expression:"schemaTitle"}})],1)],1),a("v-row",[a("v-col",[a("v-text-field",{attrs:{outlined:"",dense:"",messages:"Text prefixed to all output table names.  Defaults to no prefix.",label:"Table Prefix"},model:{value:e.table_prefix,callback:function(t){e.table_prefix=t},expression:"table_prefix"}})],1),a("v-col",[a("v-text-field",{attrs:{outlined:"",dense:"",label:"Path Seperator",placeholder:"_",messages:"Seperator between each part of the output field and table name. Defaults to `_`."},model:{value:e.path_seperator,callback:function(t){e.path_seperator=t},expression:"path_seperator"}})],1),a("v-col",[a("v-text-field",{attrs:{outlined:"",dense:"",label:"Pushdown",placeholder:"id",messages:"Field to pushdown to seperate tables"},model:{value:e.pushdown,callback:function(t){e.pushdown=t},expression:"pushdown"}})],1)],1),2!=e.panel?a("v-row",[a("v-col",[a("v-file-input",{attrs:{label:"fields.csv file",id:"fields-file",name:"fields",outlined:"",dense:"",required:""},model:{value:e.fieldsUpload,callback:function(t){e.fieldsUpload=t},expression:"fieldsUpload"}})],1),a("v-col",[a("v-checkbox",{attrs:{outlined:"",dense:"","hide-details":"true",label:"Only output fields in file"},model:{value:e.fields_only,callback:function(t){e.fields_only=t},expression:"fields_only"}})],1),a("v-col",[a("v-file-input",{attrs:{label:"tables.csv file",id:"tables-file",name:"tables",outlined:"",dense:"",required:""},model:{value:e.tablesUpload,callback:function(t){e.tablesUpload=t},expression:"tablesUpload"}})],1),a("v-col",[a("v-checkbox",{attrs:{outlined:"",dense:"","hide-details":"true",label:"Only output tables in file"},model:{value:e.tables_only,callback:function(t){e.tables_only=t},expression:"tables_only"}})],1)],1):e._e()],1)],1)],1),a("v-container",[a("v-btn",{attrs:{color:"success",disabled:e.submitButtonDisabled||"submitted"==e.formState},on:{click:e.preview}},[e._v(e._s(e.submitButtonText))]),e.apiStatus||"submitted"!=e.formState?e._e():a("v-progress-circular",{staticClass:"ml-4",attrs:{indeterminate:"",color:"grey"}})],1)],1),e.apiError?a("v-card",{directives:[{name:"intersect",rawName:"v-intersect",value:e.onIntersect,expression:"onIntersect"}],staticClass:"mt-4",attrs:{id:"error"}},[a("v-alert",{attrs:{prominent:"",type:"error"}},[e._v(" Server reported the following error: "),a("br"),a("strong",[e._v(" "+e._s(e.apiError)+" ")]),a("br"),e._v(" Try again with different options or data. ")])],1):e._e(),e.fileStart?a("v-card",{staticClass:"mt-4"},[a("v-card-title",{directives:[{name:"intersect",rawName:"v-intersect",value:e.onIntersect,expression:"onIntersect"}],attrs:{id:"input-data-preview"}},[e._v("Input data preview")]),a("v-card-text",[e._v("As the transformation failed, here is the initial part of the input file to check if it is as you expect: "),a("v-sheet",{attrs:{color:"grey lighten-3 mt-1"}},[a("pre",{staticClass:"pa-2",staticStyle:{"white-space":"pre-wrap"}},[e._v(e._s(e.fileStart))])])],1)],1):e._e(),e.apiResponse?a("v-card",{staticClass:"mt-4",attrs:{id:"success"}},[a("v-alert",{attrs:{type:"success"}},[e._v("File Processed Successfully! "),e.apiResponse.guess_text?a("small",[e._v("Guessed that data array was in "+e._s(e.apiResponse.guess_text)+" ")]):e._e()])],1):e._e(),e.apiResponse?a("v-card",{staticClass:"mt-4"},[a("v-card-title",{directives:[{name:"intersect",rawName:"v-intersect",value:e.onIntersect,expression:"onIntersect"}],attrs:{id:"tables-preview"}},[e._v("Tables Preview")]),a("v-card-text",[e._v(" Below is a preview of the tables that will be created. ")]),e._l(e.apiResponse.preview,(function(t){return a("v-container",{key:t.table_name},[a("v-card",{directives:[{name:"intersect",rawName:"v-intersect",value:e.onIntersect,expression:"onIntersect"}],attrs:{id:"table-"+t.table_name}},[a("v-card-title",{staticClass:"subtitle-1"},[e._v(" "+e._s(t.table_name)+" ")]),a("v-data-table",{attrs:{headers:e.fieldHeaders,items:t.fields,"item-key":"field_name","disable-pagination":"","hide-default-footer":""}})],1)],1)}))],2):e._e(),e.apiResponse?a("v-card",{staticClass:"mt-4",attrs:{id:"download"}},[a("v-container",[a("v-row",[a("v-col",[a("v-btn",{attrs:{color:"success",href:e.generateDownload("zip")}},[e._v("Download Full Zip")])],1),a("v-col",[a("v-btn",{attrs:{color:"success",href:e.generateDownload("xlsx")}},[e._v("Download XLSX")])],1),a("v-col",[a("v-btn",{attrs:{color:"success",href:e.generateDownload("sqlite")}},[e._v("Download SQLite")])],1),a("v-col",[a("v-btn",{attrs:{color:"success",href:e.generateDownload("csv")}},[e._v(e._s(e.main_table_name||"main")+" table as CSV")])],1),a("v-col",[a("v-btn",{attrs:{color:"success",href:e.generateDownload("fields")}},[e._v("Download fields.csv")])],1),a("v-col",[a("v-btn",{attrs:{color:"success",href:e.generateDownload("tables")}},[e._v("Download tables.csv")])],1)],1)],1)],1):e._e()],1)},S=[];a("d81d"),a("2ca0"),a("159b"),a("b64b"),a("25f0"),a("9861");function T(){return{panel:0,fileUpload:null,url:"",paste:"",useTitle:["No Title","Full Title","Slug","Underscore Slug"],arrayPosition:"top",array_key:"",path_seperator:"",table_prefix:"",schemaTitle:"No Title",json_schema:"",main_table_name:"",inline_one_to_one:!1,fieldsUpload:null,fields_only:!1,tablesUpload:null,tables_only:!1,pushdown:"",id:"",formState:"new",fileStart:"",submitType:"",apiError:"",apiResponse:null,apiStatus:null,fieldHeaders:[{text:"Field Name",value:"field_title"},{text:"Field Type",value:"field_type"},{text:"Row Count",value:"count"},{text:"Value in first row",value:"row 0"},{text:"Value in second row",value:"row 1"},{text:"Value in third row",value:"row 2"}]}}var k={name:"Home",data:T,watch:{apiError:function(e){this.$store.commit("setSection",{name:"error",value:!!e})},apiResponse:function(e){var t=!1;e&&(t=e.preview.map((function(e){return e.table_name}))),this.$store.commit("setSection",{name:"tables",value:t})},formChanged:function(){this.formState="changed",this.id="",this.fileStart="",this.submitType="",this.apiError="",this.apiResponse=null,this.apiStatus=null}},computed:{formChanged:function(){return[this.panel,this.fileUpload,this.url,this.paste,this.arrayPosition,this.array_key,this.path_seperator,this.table_prefix,this.schemaTitle,this.json_schema,this.main_table_name,this.inline_one_to_one,this.fieldsUpload,this.fields_only,this.tablesUpload,this.tables_only,this.pushdown]},submitButtonText:function(){var e={0:"Upload File and Preview",1:"Download URL and Preview",2:"Submit JSON and Preview"};return e[this.panel]},submitButtonDisabled:function(){var e={0:!!this.fileUpload,1:this.url.startsWith("http"),2:this.paste.length>5};return!e[this.panel]}},methods:{reset:function(){var e=this,t=T();Object.keys(t).forEach((function(a){return e[a]=t[a]})),this.$nextTick((function(){e.formState="new"}))},dataToParams:function(){var e={},t={"No Title":void 0,"Full Title":"full",Slug:"slug","Underscore Slug":"underscore_slug"}[this.schemaTitle];t&&(e.schema_titles=t);var a=["inline_one_to_one","main_table_name","table_prefix","path_seperator","array_key","json_schema","fields_only","tables_only","pushdown"];for(var s in a){var n=a[s];this[n]&&(e[n]=this[n])}return"stream"==this.arrayPosition&&(e["json_lines"]=!0),"top"==this.arrayPosition&&(e["array_key"]=""),e},generateDownload:function(e){var t=this.dataToParams();t.id=this.id,t.output_format=e;var a=new URLSearchParams(t).toString();return"/api/convert?"+a},preview:function(){var e=this.dataToParams();e.output_format="preview";var t={0:this.upload,1:this.downloadURL,2:this.submitPaste};t[this.panel](e)},postToApi:function(e,t){t["method"]="POST",t["headers"]["Accept"]="application/json",this.apiStatus=null,this.apiError=null,this.apiResponse=null,this.fileStart=null,this.formState="submitted",fetch("/api/convert?"+e,t).then(function(e){200!=e.status?(this.apiStatus=e.status,e.json().then(function(e){this.apiError=e.error,this.id=e.id,this.fileStart=e.start,this.$nextTick((function(){document.getElementById("error").scrollIntoView()}))}.bind(this))):(this.apiStatus=200,e.json().then(function(e){this.apiResponse=e,this.id=e.id,this.$nextTick((function(){document.getElementById("success").scrollIntoView()}))}.bind(this)))}.bind(this))},uploadFormData:function(e){var t=new FormData;return e&&t.append("file",this.fileUpload),this.fieldsUpload&&t.append("fields",this.fieldsUpload),this.tablesUpload&&t.append("tables",this.tablesUpload),t},upload:function(e){var t=new URLSearchParams(e).toString(),a=this.uploadFormData(!0),s={headers:{},body:a};this.postToApi(t,s),this.submitType="upload"},downloadURL:function(e){e.file_url=this.url;var t=new URLSearchParams(e).toString(),a=this.uploadFormData(!1),s={headers:{},body:a};this.postToApi(t,s),this.submitType="url"},submitPaste:function(e){var t=new URLSearchParams(e).toString(),a={headers:{"Content-Type":"application/json"},body:this.paste};this.postToApi(t,a),this.submitType="paste"},onIntersect:function(e){e[0].isIntersecting&&this.$store.commit("setListItem",e[0].target.id)}}},P=k,I=a("0798"),U=a("8336"),V=a("b0af"),j=a("99d9"),C=a("ac7c"),O=a("62ad"),D=a("a523"),R=a("8fea"),L=a("cd55"),N=a("49e2"),E=a("c865"),F=a("0393"),A=a("23a7"),$=a("490a"),J=a("67b6"),B=a("43a6"),H=a("0fd9"),M=a("b974"),q=a("8dd9"),G=a("8654"),W=a("a844"),X=a("269a"),z=a.n(X),K=a("90a2"),Q=Object(l["a"])(P,g,S,!1,null,null,null),Z=Q.exports;u()(Q,{VAlert:I["a"],VBtn:U["a"],VCard:V["a"],VCardText:j["a"],VCardTitle:j["b"],VCheckbox:C["a"],VCol:O["a"],VContainer:D["a"],VDataTable:R["a"],VExpansionPanel:L["a"],VExpansionPanelContent:N["a"],VExpansionPanelHeader:E["a"],VExpansionPanels:F["a"],VFileInput:A["a"],VProgressCircular:$["a"],VRadio:J["a"],VRadioGroup:B["a"],VRow:H["a"],VSelect:M["a"],VSheet:q["a"],VTextField:G["a"],VTextarea:W["a"]}),z()(Q,{Intersect:K["a"]}),s["a"].use(x["a"]);var Y=[{path:"/",name:"Home",component:Z},{path:"/about",name:"About",component:function(){return a.e("about").then(a.bind(null,"f820"))}}],ee=new x["a"]({mode:"history",base:"/",routes:Y}),te=ee,ae=a("f309");s["a"].use(ae["a"]);var se=new ae["a"]({}),ne=(a("b0c0"),a("2f62"));s["a"].use(ne["a"]);var ie=new ne["a"].Store({state:{sections:{error:!1,tables:!1},listItem:"json-input"},mutations:{setSection:function(e,t){this.state.sections[t.name]=t.value},setListItem:function(e,t){this.state.listItem=t}},actions:{},modules:{}});s["a"].config.productionTip=!1,new s["a"]({router:te,vuetify:se,store:ie,render:function(e){return e(y)}}).$mount("#app")}});
//# sourceMappingURL=app.0d2f5f30.js.map