import{b as o,d as t,n as i,s as e,y as n,U as s,j as a}from"./index-99c4f288.js";import"./c.b803e671.js";import"./c.a70a794b.js";let l=class extends e{render(){return n`
      <esphome-process-dialog
        .heading=${`Clean ${this.configuration}`}
        .type=${"clean"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){s(this.configuration)}_openInstall(){a(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],l.prototype,"configuration",void 0),l=o([i("esphome-clean-dialog")],l);
