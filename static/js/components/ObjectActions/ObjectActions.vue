<script>

// import PlayerControlApp from '../../apps/player/player-control-app';
import ClickOutside from 'vue-click-outside';
import ObjectActionsAction from './ObjectActionsAction.vue';
import ObjectActionsPlay from './ObjectActionsPlay.vue';

export default {
  name: 'ObjectActions',
  components: {
    action: ObjectActionsAction,
    play: ObjectActionsPlay,
  },
  directives: {
    ClickOutside,
  },
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    ct: {
      type: String,
      required: true,
    },
    uuid: {
      type: String,
      required: true,
    },
    url: {
      type: String,
      required: true,
    },
    editUrl: {
      type: String,
      default: null,
    },
    canPlay: {
      type: Boolean,
      default: false,
    },
    canQueue: {
      type: Boolean,
      default: false,
    },
    canDownload: {
      type: Boolean,
      default: false,
    },
    canEdit: {
      type: Boolean,
      default: false,
    },
    canSchedule: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      secondaryActionsVisible: false,
    };
  },
  computed: {
    actions() {
      const actions = [];

      if (this.canQueue) {
        actions.push({
          key: 'queue',
          icon: 'fa-pause',
          title: 'Queue',
        });
      }

      if (this.canDownload) {
        actions.push({
          key: 'download',
          icon: 'fa-download',
          title: 'Download',
        });
      }

      if (this.canEdit) {
        actions.push({
          key: 'edit',
          icon: 'fa-pencil',
          title: 'Edit',
        });
      }

      if (this.canSchedule) {
        actions.push({
          key: 'clipboard',
          icon: 'fa-calendar',
          title: 'Add to scheduler',
        });
      }

      return actions;
    },
  },
  mounted() {
    // this.playerControl = new PlayerControlApp();
  },
  methods: {
    toggleSecondaryActions(e) {
      this.secondaryActionsVisible = !this.secondaryActionsVisible;
    },
    hideSecondaryActions(e, el) {
      console.debug(el, e, 'click outside...');
    },
    handleAction(key) {
      this.secondaryActionsVisible = false;

      // TODO: handle actions...
      if (key === 'play') {
        this.playerControls({
          do: 'load',
          // opts: {
          //   mode: 'queue',
          // },
          items: [{
            ct: this.ct,
            uuid: this.uuid,
          }],
        });
      }
      if (key === 'queue') {
        this.playerControls({
          do: 'load',
          opts: {
            mode: 'queue',
          },
          items: [{
            ct: this.ct,
            uuid: this.uuid,
          }],
        });
      }
      if (key === 'edit') {
        document.location.href = this.editUrl;
      }

      if (key === 'clipboard') {
        const co = {
          name: '...loading...',
          ct: this.ct,
          uuid: this.uuid,
          url: this.url,
        };
        this.$store.dispatch('scheduler/addToClipboard', co);
      }
    },
    playerControls(action) {
      const e = new CustomEvent('player:controls', { detail: action });
      window.dispatchEvent(e);
    },
  },
};
</script>
<style lang="scss" scoped>
    .object-actions {
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: center;
      width: 100%;
      height: 100%;
      opacity: 0;

      &:hover {
        background: rgba(#000, 0.5);
        opacity: 1;
      }

      .actions {
        // background: rgba(#000, .5);
        display: flex;
        justify-content: center;

        .action {
          margin: 0 8px;
          color: #fff;
          font-size: 32px;
          cursor: pointer;

          &--primary {
            width: 48%;

            .circle-button {
              display: block;
              width: 60px;
              height: 60px;
              background: black;
              border-radius: 30px;
            }
          }

          &--secondary {
            width: 24%;
          }
        }
      }

      .secondary-actions {
        position: absolute;
        top: 55%;
        right: 4px;
        z-index: 999;
        display: flex;
        flex-direction: column;
        filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.1));

        &__triangle {
          width: 20px;
          height: 10px;
          margin: 0 auto;
          background: white;
          opacity: 0;
          clip-path: polygon(50% 0%, 100% 100%, 0 100%);
        }

        &__list {
          background: white;
        }
      }
    }
</style>

<template>
  <div
    class="object-actions"
  >
    <div
      :style="{transform: `scale(${scale})`}"
      class="actions"
    >
      <div
        class="action action--secondary"
      >
        <div />
      </div>
      <div
        class="action action--primary"
      >
        <play
          v-if="canPlay"
          @click="handleAction('play')"
        />
      </div>
      <div
        class="action action--secondary"
      >
        <div
          v-if="(actions && actions.length)"
          @click="toggleSecondaryActions"
        >
          <i class="fa fa-ellipsis-h" />
        </div>
      </div>
    </div>
    <div
      v-if="secondaryActionsVisible"
      v-click-outside="hideSecondaryActions"
      class="secondary-actions"
    >
      <div class="secondary-actions__triangle" />
      <div
        v-for="action in actions"
        :key="action.key"
        class="secondary-actions__list"
      >
        <action
          :action="action"
          @click="handleAction(action.key)"
        />
      </div>
    </div>
  </div>
</template>
