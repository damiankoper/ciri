<template>
  <div>
    The price of the {{ message.payload.name }} ({{ message.payload.ticker }})
    is {{ message.payload.price }}
    {{ message.payload.currency.toUpperCase() }} as of
    {{ DateTime.fromSeconds(message.payload.time).toRelativeCalendar() }}.
    <br />
    <el-link
      :href="
        'https://www.tradingview.com/chart?symbol=' + message.payload.ticker
      "
      target="_blank"
      style="color: white"
    >
      <i class="mdi mdi-open-in-new" /> Go to price chart
    </el-link>
  </div>
</template>

<script setup lang="ts">
import { PropType } from 'vue';
import { StockMessage } from 'apps/web/src/domain/chat/models/stock-message.model';
import { DateTime } from 'luxon';

defineProps({
  message: {
    type: Object as PropType<StockMessage>,
    required: true,
  },
});
</script>
