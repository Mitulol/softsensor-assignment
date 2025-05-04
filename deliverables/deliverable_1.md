## logistics_companies
```
_id: string (e.g., "company_001")
name: string
region: string
fleet: array of vehicle_id -> cross-ref: vehicles._id
drivers: array of driver_id -> cross-ref: drivers._id
active_zones: array of zone_id -> cross-ref: zones._id
```

### nesting depth: 2. 
I saw a lot of documentation. Some of them consider an array to be
at a higher nesting depth. I have assumed the same.

### Sample:
```json
{
  "_id": "company_001",
  "name": "Express Logistics Co.",
  "region": "North-East USA",
  "fleet": ["veh_1001", "veh_1002"],
  "drivers": ["drv_5001", "drv_5002"],
  "active_zones": ["zone_A", "zone_B"]
}
```

## vehicles
_id: string
type: string
capacity_packages: integer
maintenance_logs[]
    service_date: string
    details.km_reading: int
    details.tasks[]: task + cost
sensor_streams[]
    stream_type: string
    points[][] or readings[]: nested arrays of timestamps and measurements
current_assignments[]
    route_id
    start_date
    details.planned_stops[] -> ref: stops._id
    details.backup_vehicles[] -> ref: vehicles._id

### nesting depth: 6. 
maintenance_logs contains an array of objects.
Each object is at depth 2, details at depth 3, tasks at depth 4, 
each object in tasks array at 5, and task and cost at 6.

### Sample:

```json
{
  "_id": "veh_1001",
  "type": "Van",
  "capacity_packages": 200,
  "maintenance_logs": [
    {
      "service_date": "2025-04-15",
      "details": {
        "km_reading": 54321,
        "tasks": [
          { "task": "Oil Change", "cost": 120 },
          { "task": "Brake Inspection", "cost": 80 }
        ]
      }
    },
    {
      "service_date": "2025-07-15",
      "details": {
        "km_reading": 54421,
        "tasks": [
          { "task": "Oil Change", "cost": 120 },
          { "task": "Brake Inspection", "cost": 80 }
        ]
      }
    }
  ],
  "sensor_streams": [
    {
      "stream_type": "gps",
      "points": [[
        { "ts": "2025-05-01T08:05:00Z", "lat": 40.7128, "lng": -74.006 },
        { "ts": "2025-05-01T08:15:00Z", "lat": 40.715, "lng": -74.01 }
      ]]
    },
    {
      "stream_type": "fuel",
      "readings": [
          {"ts": "2025-05-01T09:00:00Z", "liters": 4.1},
          {"ts": "2025-05-01T12:00:00Z", "liters": 3.9}
        ]
    }
  ],
  "current_assignments": [
    {
      "route_id": "rte_9001",
      "start_date": "2025-05-01",
      "details": {
        "planned_stops": ["stop_1", "stop_2"],
        "backup_vehicles": ["veh_1002"]
      }
    },
    {
      "route_id": "rte_9001",
      "start_date": "2025-09-01",
      "details": {
        "planned_stops": ["stop_1", "stop_2"],
        "backup_vehicles": ["veh_1002"]
      }
    }
  ]
}
```

## drivers
_id: string
name: string
license.class / expiry
certifications[]
    type: string
    levels[]: string
weekly_schedule[]
    day
    shifts[]: start/end times

### nesting depth: 5. 
weekly_schedule at 1, has array of object each at depth 2,
shifts inside object at depth 3,
which has array of objects each at depth 4,
and start inside the object at depth 5.

### Sample:

```json
{
  "_id": "drv_5001",
  "name": "Alice Chen",
  "license": {
    "class": "Class C",
    "expiry": "2026-02-28"
  },
  "certifications": [
    {
      "type": "Safety",
      "levels": ["Basic", "Advanced"]
    },
    {
      "type": "Hazmat",
      "levels": ["Basic", "Advanced"]
    }
  ],
  "weekly_schedule": [
    {
      "day": "Mon",
      "shifts": [
        { "start": "08:00", "end": "16:00" },
        { "start": "18:00", "end": "22:00" }
      ]
    },
    {
      "day": "Tue",
      "shifts": [
        { "start": "08:00", "end": "16:00" },
        { "start": "18:00", "end": "22:00" }
      ]
    }
  ]
}
```


## stops
_id: string
package_id: string
address: string
events[]
    type: arrival / delivery_attempts
    ts or attempts[] with ts, status & optional exception
customer_callbacks[]
    callback_ts
    issues[]: type + detail

### nesting depth: 6. 
events at 1, has as array of objects each at 2, attempts at 3,
has an array of object each at 4, exception at 5, code at 6

### Sample:

```json
{
  "_id": "stop_1",
  "package_id": "pkg_201",
  "address": "123 Maple St, Newark, NJ",
  "events": [
    { "type": "arrival", "ts": "2025-05-01T08:25:00Z" },
    {
      "type": "delivery_attempts",
      "attempts": [
        {
          "ts": "2025-05-01T08:30:00Z",
          "status": "Exception",
          "exception": {
            "code": "NO_ACCESS",
            "reason": "Gate locked"
          }
        },
        {
          "ts": "2025-05-01T09:00:00Z",
          "status": "Delivered"
        }
      ]
    },
    { "type": "arrival", "ts": "2025-06-01T08:25:00Z" },
    {
      "type": "delivery_attempts",
      "attempts": [
        {
          "ts": "2025-06-01T08:30:00Z",
          "status": "Exception",
          "exception": {
            "code": "NO_ACCESS",
            "reason": "Gate locked"
          }
        },
        {
          "ts": "2025-07-01T09:00:00Z",
          "status": "Delivered"
        }
      ]
    }

  ],
  "customer_callbacks": [
    {
      "callback_ts": "2025-05-02T12:00:00Z",
      "issues": [
        {
          "type": "missing_item",
          "detail": "Wrong SKU"
        }
        {
          "type": "damahed_item",
          "detail": "damaged product"
        }
      ]
    }
  ]
}
```

## zones
_id: string
name: string
boundaries[][]: array of array of points (polygon rings)
subzones[]
    id, name

### nesting depth: 4. 
boundaries is depth 1, inner array depth 2, object is depth 3 and
lat and long are depth 4.

### Sample:

```json
{
  "_id": "zone_A",
  "name": "Central Zone",
  "boundaries": [
    [
      { "lat": 40.73, "lng": -74.18 },
      { "lat": 40.74, "lng": -74.16 },
      { "lat": 40.75, "lng": -74.17 }
    ],
    [
      { "lat": 40.735, "lng": -74.17 },
      { "lat": 40.736, "lng": -74.165 },
      { "lat": 40.737, "lng": -74.178 }
    ]
  ],
  "subzones": [
    {
      "id": "zone_A1",
      "name": "Warehouse District"
    },
    {
      "id": "zone_A2",
      "name": "Hospital District"
    }
  ]
}
```

## inspections
_id: string
date
inspector.id / name
vehicle_id -> ref: vehicles._id
checklist[]: item, status, optional notes
issues_found[]: code + description

### nesting depth: 3
checklist at 1, objects inside array at 2, item and status at 3.

### Sample:

```json
{
  "_id": "insp_1001",
  "date": "2025-05-01",
  "inspector": {
    "id": "emp_203",
    "name": "Emily Davis"
  },
  "vehicle_id": "veh_1001",
  "checklist": [
    { "item": "Brakes", "status": "Pass" },
    { "item": "Lights", "status": "Fail", "notes": "Left headlight out" }
  ],
  "issues_found": [
    {
      "code": "BRK01",
      "description": "Brake pad wear"
    }
  ]
}
```