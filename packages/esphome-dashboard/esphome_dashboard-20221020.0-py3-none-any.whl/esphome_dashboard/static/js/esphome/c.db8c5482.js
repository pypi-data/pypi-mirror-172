import{r as o,b as e,d as t,p as i,n as r,s,y as a}from"./index-99c4f288.js";import"./c.b803e671.js";import{o as n}from"./c.5c179fc2.js";import{e as c}from"./c.4fceb30e.js";import"./c.a70a794b.js";import"./c.ea50bec1.js";import"./c.36245e7b.js";import"./c.2e012194.js";import"./c.20b57887.js";let d=class extends s{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return a`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?a`
              <a
                slot="secondaryAction"
                href="${c(this.configuration,this.downloadFactoryFirmware)}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const e=document.createElement("a");e.download=this.configuration+".bin",e.href=c(this.configuration,this.downloadFactoryFirmware),document.body.appendChild(e),e.click(),e.remove()}_handleRetry(){n(this.configuration,this.downloadFactoryFirmware)}_handleClose(){this.parentNode.removeChild(this)}};d.styles=o`
    a {
      text-decoration: none;
    }
  `,e([t()],d.prototype,"configuration",void 0),e([t()],d.prototype,"downloadFactoryFirmware",void 0),e([i()],d.prototype,"_result",void 0),d=e([r("esphome-compile-dialog")],d);
