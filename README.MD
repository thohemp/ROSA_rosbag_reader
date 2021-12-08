
## Fix ros message definition inside rosbags

```
python fix_bag_msg_def.py --inbag input.bag --outbag output.bag
```


## Output basic rosbag info
```sh
python rosa_rosbag_reader.py --bag input.bag --info
```

## Print topic to console
```sh
python rosa_rosbag_reader.py --bag result.bag --topic /WS1/attention --print
```
    # =======================================
    # topic:           /WS1/attention
    # msg_count:       1
    # timestamp (sec): 1634889805.310080290
    # - - -
    data: -128

    # =======================================
    # topic:           /WS1/attention
    # msg_count:       2
    # timestamp (sec): 1634889807.407074451
    # - - -
    data: 14
    ...


## Write topic to CSV
```sh
python rosa_rosbag_reader.py --bag result.bag --topic /WS1/attention --export #(optional --export_name) for defining the target file name.
```

## Export all known topics to CSV
```sh
python rosa_rosbag_reader.py --bag result.bag --export_all
```

## Supported topics for export:
- /WS1/attention
- /WS1/attention_visual
- /WS1/borderless/commands
- /WS1/reco_stt
- /WS1/activebody
