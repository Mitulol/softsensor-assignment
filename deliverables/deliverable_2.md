# Airbyte Connection Configuration

I tried setting up `abctl` with Airbyte on my personal laptop, but it kept installing for hours. 
In the end it took somewhere around **10-12** hours on my personal laptop. So I decided to use **Airbyte Cloud** instead. 
It doesn’t have a way to export the connection config, but I was able to export the **source config** and **destination config** separately.  
I hope that’s the config you were referring to.



## Source: MongoDB (Atlas) `cloud.mongodb.com`

```json
{
  "name": "MongoDb",
  "workspaceId": "840d8796-5be3-4daf-a59b-985eb1c459dc",
  "definitionId": "b2e713cd-cc36-4c0a-b5bd-b47cb8a0561e",
  "configuration": {
    "queue_size": 10000,
    "database_config": {
      "database": "softsensor",
      "password": "******",
      "username": "mitgoel",
      "auth_source": "admin",
      "cluster_type": "ATLAS_REPLICA_SET",
      "schema_enforced": true,
      "connection_string": "mongodb+srv://mitgoel:mitul@cluster0.znrp0w5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    },
    "update_capture_mode": "Lookup",
    "discover_sample_size": 10000,
    "initial_waiting_seconds": 300,
    "discover_timeout_seconds": 600,
    "initial_load_timeout_hours": 8,
    "invalid_cdc_cursor_position_behavior": "Fail sync"
  }
}
```

## Destination: PostgreSQL (Supabase) `supabase.com`

```json
{
  "name": "Postgres",
  "workspaceId": "840d8796-5be3-4daf-a59b-985eb1c459dc",
  "definitionId": "25c5221d-dce2-4163-ade9-739ef790f503",
  "configuration": {
    "host": "aws-0-us-east-2.pooler.supabase.com",
    "port": 5432,
    "schema": "public",
    "database": "postgres",
    "password": "******",
    "ssl_mode": {
      "mode": "require"
    },
    "username": "postgres.tnnyyivccusysyoabgtz",
    "drop_cascade": false,
    "tunnel_method": {
      "tunnel_method": "NO_TUNNEL"
    },
    "disable_type_dedupe": false,
    "unconstrained_number": false
  }
}
```

# Sync Log

![Sync log 1](deliverable_2_sync_log_1.png)

![Sync log 2](deliverable_2_sync_log_2.png)



