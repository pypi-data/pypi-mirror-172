import{_ as e,e as i,t,i as s,a7 as a,y as d,J as o,n,j as c}from"./main-22e4648c.js";import"./c.fa63af8a.js";import{c as l}from"./c.d2f13ac1.js";import{s as r}from"./c.874c8cfd.js";import{a as h,s as u,b as v,d as m}from"./c.f0a491f8.js";import{S as k}from"./c.3704df89.js";import"./c.35d79203.js";const f=e=>d`<mwc-list-item
  .twoline=${!!e.area}
>
  <span>${e.name}</span>
  <span slot="secondary">${e.area}</span>
</mwc-list-item>`;e([n("ha-device-picker")],(function(e,n){return{F:class extends n{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i()],key:"devices",value:void 0},{kind:"field",decorators:[i()],key:"areas",value:void 0},{kind:"field",decorators:[i()],key:"entities",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[i()],key:"deviceFilter",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:void 0},{kind:"field",decorators:[t()],key:"_opened",value:void 0},{kind:"field",decorators:[s("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value:()=>!1},{kind:"field",key:"_getDevices",value(){return a(((e,i,t,s,a,d,o)=>{if(!e.length)return[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_devices")}];const n={};if(s||a||d)for(const e of t)e.device_id&&(e.device_id in n||(n[e.device_id]=[]),n[e.device_id].push(e));const c={};for(const e of i)c[e.area_id]=e;let u=e.filter((e=>e.id===this.value||!e.disabled_by));s&&(u=u.filter((e=>{const i=n[e.id];return!(!i||!i.length)&&n[e.id].some((e=>s.includes(l(e.entity_id))))}))),a&&(u=u.filter((e=>{const i=n[e.id];return!i||!i.length||t.every((e=>!a.includes(l(e.entity_id))))}))),d&&(u=u.filter((e=>{const i=n[e.id];return!(!i||!i.length)&&n[e.id].some((e=>{const i=this.hass.states[e.entity_id];return!!i&&(i.attributes.device_class&&d.includes(i.attributes.device_class))}))}))),o&&(u=u.filter((e=>e.id===this.value||o(e))));const v=u.map((e=>({id:e.id,name:h(e,this.hass,n[e.id]),area:e.area_id&&c[e.area_id]?c[e.area_id].name:this.hass.localize("ui.components.device-picker.no_area")})));return v.length?1===v.length?v:v.sort(((e,i)=>r(e.name||"",i.name||""))):[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_match")}]}))}},{kind:"method",key:"open",value:function(){var e;null===(e=this.comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:function(){var e;null===(e=this.comboBox)||void 0===e||e.focus()}},{kind:"method",key:"hassSubscribe",value:function(){return[u(this.hass.connection,(e=>{this.devices=e})),v(this.hass.connection,(e=>{this.areas=e})),m(this.hass.connection,(e=>{this.entities=e}))]}},{kind:"method",key:"updated",value:function(e){(!this._init&&this.devices&&this.areas&&this.entities||e.has("_opened")&&this._opened)&&(this._init=!0,this.comboBox.items=this._getDevices(this.devices,this.areas,this.entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter))}},{kind:"method",key:"render",value:function(){return this.devices&&this.areas&&this.entities?d`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):this.label}
        .value=${this._value}
        .helper=${this.helper}
        .renderer=${f}
        .disabled=${this.disabled}
        .required=${this.required}
        item-value-path="id"
        item-label-path="name"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._deviceChanged}
      ></ha-combo-box>
    `:d``}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();let i=e.detail.value;"no_devices"===i&&(i=""),i!==this._value&&this._setValue(i)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{o(this,"value-changed",{value:e}),o(this,"change")}),0)}}]}}),k(c));
