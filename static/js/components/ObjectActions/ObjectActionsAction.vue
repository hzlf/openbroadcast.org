<script>

export default {
  name: 'ObjectActionsAction',
  props: {
    action: {
      type: Object,
      required: true,
    },
  },
};
</script>
<style lang="scss" scoped>
    .action {
      display: flex;
      min-width: 120px;
      padding: 8px 12px;
      cursor: pointer;

      &:hover {
        color: #fff;
        background: #00bb73;
      }

      &__icon {
        width: 20px;
      }

      &__name {
        flex-grow: 1;
        white-space: nowrap;
      }
    }
</style>

<template>
  <div
    class="action"
    @click="$emit('click')"
  >
    <div class="action__icon">
      <i
        :class="action.icon"
        class="fa"
      />
    </div>
    <div class="action__name">
      {{ action.title }}
    </div>
  </div>
</template>
