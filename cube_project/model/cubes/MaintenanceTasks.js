cube(`MaintenanceTasks`, {
  sql: `SELECT * FROM softsensor.fct_maintenance_tasks`,

  measures: {
    maintenanceCostTotal: {
      sql: `total_maintenance_cost`,
      type: `sum`,
      title: `Total Maintenance Cost`
    }
  },

  dimensions: {
    serviceDate: {
      sql: `service_date`,
      type: `time`
    }
  }
});
