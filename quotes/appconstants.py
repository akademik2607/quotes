TransportTypes = (
    ('TR', 'tractor'),
    ('CA', 'car')
)

nullable = {
    'null': True,
    'blank': True
}


SERVICE_TYPES = (
    ('Door to Door', 'Door to Door'),
    ('Door to Port', 'Door to Port'),
    ('Port to Door', 'Port to Door'),
    ('Port to Port', 'Port to Port'),
)

SERVICES = (
    ('origin_services', 'Origin Services'),
    ('international_freight', 'International Freight'),
    ('destination_services', 'Destination Services'),
    ('add', 'add')
)

METHODS = (
    ('Sea', 'Sea'),
    ('Air', 'Air')
)

FREIGHT_MODES = (
    ('Air', 'Air'),
    ('LCL', 'LCL'),
    ("FCL 20'ft", "FCL 20'ft"),
    ("FCL 40'ft", "FCL 40'ft"),
    ("FCL 40'HC", "FCL 40'HC")
)