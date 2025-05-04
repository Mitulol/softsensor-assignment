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
  