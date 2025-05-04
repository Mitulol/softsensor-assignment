cube(`InspectionSummary`, {
  sql: `SELECT * FROM softsensor.fct_inspection_summary`,

  measures: {
    totalChecks: {
      sql: `total_checks`,
      type: `sum`
    },

    failedChecks: {
      sql: `failed_checks`,
      type: `sum`
    },

    inspectionPassRate: {
      sql: `(${totalChecks} - ${failedChecks}) * 1.0 / NULLIF(${totalChecks}, 0)`,
      type: `number`,
      format: `percent`,
      title: `Inspection Pass Rate`
    }
  },

  dimensions: {
    inspectionDate: {
      sql: `inspection_date`,
      type: `time`
    }
  }
});
