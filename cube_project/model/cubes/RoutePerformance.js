cube(`RoutePerformance`, {
  sql: `SELECT * FROM softsensor.fct_route_performance`,

  measures: {
    completedDeliveries: {
      sql: `completed_deliveries`,
      type: `sum`
    },

    plannedStops: {
      sql: `planned_stop_count`,
      type: `sum`
    },

    exceptionCount: {
      sql: `exception_count`,
      type: `sum`,
      title: `Exception Count`
    },

    deliverySuccessRate: {
      sql: `${completedDeliveries} * 100.0 / NULLIF(${plannedStops}, 0)`,
      type: `number`,
      format: `percent`,
      title: `Delivery Success Rate`
    }
  },

  dimensions: {
    startDate: {
      sql: `start_date`,
      type: `time`
    }
  }
});
