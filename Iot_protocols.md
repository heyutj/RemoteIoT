# 控制协议

|种类|值|
|---|---|
|type|ctrl|
|device_type|video/audio/light/switch|
|device_id|int number|


``` json
example:
{
    "type":"ctrl",
    "device_type":"video",
    "device_id":"id",
    "action":"on"
}
```