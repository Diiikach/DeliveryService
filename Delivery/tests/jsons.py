valid_courier_json_load = """
{
"data": [
{
    "courier_id": 1,
    "courier_type": "foot",
    "regions": [1, 12, 22],
    "working_hours": ["11:35-14:05", "09:00-11:00"]
},
{
    "courier_id": 2,
    "courier_type": "bike",
    "regions": [22],
    "working_hours": ["09:00-18:00"]
}
]
}
"""

valid_courier_json_ans = '{"couriers": [{"id": 1}, {"id": 2}]}'

fully_unvalid_courier_json_load = """
{
"data": [
{
"courier_id": 1,
"courier_type": "foot",
"regions": [1, 12, 22],
"working_hours": ["11:35-14:05", "09:00-11:00"]
},
{
"courier_id": 2,
"courier_type": "bike",
"regions": [22],
"working_hours": ["09:00-18:00"]
},
{
"courier_id": 3,
"courier_type": "car",
"regions": [12, 22, 23, 33],
"working_hours": []
},
...
]
}
"""

parially_courier_json_load = """
    {
"data": [
{
"courier_id": 1,
"courier_type": "foot",
"regions": [1, 12, 22],
"working_hours": ["11:35-14:05", "09:00-11:00"]
},
{
"courier_id": 2,

"working_hours": ["09:00-18:00"]
}]}
"""

parially_courier_json_ans = '{"ValidationError": {"couriers": [{"id": 2}]}}'

change_courier_regions_valid = """
{
"regions": [11, 33, 2]
}
"""

change_courier_regions_valid_ans = '{"courier_id": 1, "courier_type": "foot", "regions": [11, 33, 2], "working_hours": ["11:35-14:05", "09:00-11:00"]}'

change_courier_wh_valid = """
{
    "working_hours": ["12:00-22:00"]
}
"""

change_courier_wh_valid_ans = '{"courier_id": 1, "courier_type": "foot", "regions": [1, 12, 22], "working_hours": ["12:00-22:00"]}'

change_courier_type_valid = """
{
    "courier_type": "car"
    }
"""

change_courier_type_valid_ans =  '{"courier_id": 1, "courier_type": "car", "regions": [1, 12, 22], "working_hours": ["11:35-14:05", "09:00-11:00"]}'

valid_orders_json_load = """
   {
"data": [
{
"order_id": 1,
"weight": 0.23,
"region": 12,
"delivery_hours": ["09:00-18:00"]
},
{
"order_id": 2,
"weight": 15,
"region": 1,
"delivery_hours": ["09:00-18:00"]
},
{
"order_id": 3,
"weight": 0.01,
"region": 22,
"delivery_hours": ["09:00-12:00", "16:00-21:30"]
}
]
} 
"""

valid_orders_json_ans = '{"orders": [{"id": 1}, {"id": 2}, {"id": 3}]}'

invalid_orders_json_load = """
   {
"data": [
{
"order_id": 1,
"weight": 0.23,
"region": 12,
"delivery_hours": ["09:00-18:00"]
},
{
"order_id": 2,
"weight": 15,
"region": 1,
"delivery_hours": ["09:00-18:00"]
},
{
"order_id": 3,
"weight": 0.01,
"region": 22,
"delivery_hours": ["09:00-12:00", "16:00-21:30"]
}

"""

partialy_invalid_orders_json_load = """
   {
"data": [
{
"order_id": 1,
"weight": 0.23,
"region": 12,
"delivery_hours": ["09:00-18:00"]
},
{
"order_id": 2,
"delivery_hours": ["09:00-18:00"],
}
]}
"""

courier_json_to_assign_orders = """
{
    "data": [
{
    "courier_id": 1,
    "courier_type": "car",
    "regions": [1, 12, 22],
    "working_hours": ["11:35-14:05", "09:00-11:00"]
}]}
"""

orders_json_to_assign = """
       {
"data": [
{
"order_id": 1,
"weight": 0.23,
"region": 12,
"delivery_hours": ["09:00-18:00"]
},
{
"order_id": 2,
"weight": 15,
"region": 1,
"delivery_hours": ["09:00-18:00"]
},
{
"order_id": 3,
"weight": 0.01,
"region": 22,
"delivery_hours": ["09:00-12:00", "16:00-21:30"]
}
]
} 
"""

courier_json_to_assign_orders_id = """
    {    
    "courier_id": 1
    }
"""

valid_assigned_orders = """
{"orders": [{"id": 1}, {"id": 2}, {"id": 3}], "assign_time": "2021-03-29 01:18:49.656657+00:00"}
"""

complete_order_1 = """
        {
"courier_id": 1,
"order_id": 1,
"complete_time": "2021-01-10T23:33:01.42Z"
}
"""

complete_order_2 = """
        {
"courier_id": 1,
"order_id": 2,
"complete_time": "2021-01-10T10:55:01.42Z"
}
"""

complete_order_3 = """
        {
"courier_id": 1,
"order_id": 3,
"complete_time": "2021-01-10T11:33:01.42Z"
}
"""

changed_type_courier = """
{
    "courier_type": "foot"
    }
"""

valid_full_user_ifo = '{"courier_id": 1, "courier_type": "foot", "regions": [1, 12, 22], "working_hours": ["11:35-14:05", "09:00-11:00"], "earning": 0}'

load_couriers_final = """
    {
    "data": [
{
    "courier_id": 1,
    "courier_type": "car",
    "regions": [1, 12, 22]
}]}
"""

load_orders_final = """
{
 "data": [
        {
            "order_id": 1,
            "weight": 30,
            "region": 12,
            "delivery_hours": ["10:00-11:00"]
        },
        {
            "order_id": 2,
            "weight": 5,
            "region": 22,
            "delivery_hours": ["10:00-12:00"]
        },
        {
            "order_id": 3,
            "weight": 45,
            "region": 12,
            "delivery_hours": ["09:00-15:30"]
        }

    ]
    }
"""

load_orders_final2 = """
{
 "data": [
        {
            "order_id": 1,
            "weight": 30,
            "region": 12,
            "delivery_hours": ["10:00-11:00"]
        },
        {
            "order_id": 2,
            "weight": 4,
            "region": 22,
            "delivery_hours": ["10:00-12:00"]
        },
        {
            "order_id": 3,
            "weight": 3,
            "region": 12,
            "delivery_hours": ["09:00-15:30"]
        },
        {
            "order_id": 4,
            "weight": 3,
            "region": 22,
            "delivery_hours": ["09:00-15:30"]
        }

    ]
    }
"""


current_assign_resp = '{"orders": [{"id": 2}, {"id": 3}], "assign_time": "2021-03-29T18:04:00.973003+00:00"]}'
current_full_info_ans = '{"courier_id": 1, "courier_type": "car", "regions": [1, 12, 22], "working_hours": ["11:35-14:05", "09:00-11:00"], "rating": 5.0, "earning": 4500}'

complete_order_4 = """
        {
"courier_id": 1,
"order_id": 4,
"complete_time": "2021-03-31T23:33:01.42Z"
}
"""