import json

TOOL_INFO = [{'type': 'function', 'function': {'name': 'calculate', 'description': 'Calculate the result of a mathematical expression.', 'parameters': {'type': 'object', 'properties': {'expression': {'type': 'string', 'description': "The mathematical expression to calculate, such as '2 + 2'. The expression can contain numbers, operators (+, -, *, /), parentheses, and spaces."}}, 'required': ['expression']}}}, {'type': 'function', 'function': {'name': 'cancel_pending_order', 'description': "Cancel a pending order. If the order is already processed or delivered, it cannot be cancelled. The agent needs to explain the cancellation detail and ask for explicit user confirmation (yes/no) to proceed. If the user confirms, the order status will be changed to 'cancelled' and the payment will be refunded. The refund will be added to the user's gift card balance immediately if the payment was made using a gift card, otherwise the refund would take 5-7 business days to process. The function returns the order details after the cancellation.", 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': "The order id, such as '#W0000000'. Be careful there is a '#' symbol at the beginning of the order id."}, 'reason': {'type': 'string', 'enum': ['no longer needed', 'ordered by mistake'], 'description': "The reason for cancellation, which should be either 'no longer needed' or 'ordered by mistake'."}}, 'required': ['order_id', 'reason']}}}, {'type': 'function', 'function': {'name': 'exchange_delivered_order_items', 'description': 'Exchange items in a delivered order to new items of the same product type. For a delivered order, return or exchange can be only done once by the agent. The agent needs to explain the exchange detail and ask for explicit user confirmation (yes/no) to proceed.', 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': "The order id, such as '#W0000000'. Be careful there is a '#' symbol at the beginning of the order id."}, 'item_ids': {'type': 'array', 'items': {'type': 'string'}, 'description': "The item ids to be exchanged, each such as '1008292230'. There could be duplicate items in the list."}, 'new_item_ids': {'type': 'array', 'items': {'type': 'string'}, 'description': "The item ids to be exchanged for, each such as '1008292230'. There could be duplicate items in the list. Each new item id should match the item id in the same position and be of the same product."}, 'payment_method_id': {'type': 'string', 'description': "The payment method id to pay or receive refund for the item price difference, such as 'gift_card_0000000' or 'credit_card_0000000'. These can be looked up from the user or order details."}}, 'required': ['order_id', 'item_ids', 'new_item_ids', 'payment_method_id']}}}, {'type': 'function', 'function': {'name': 'find_user_id_by_email', 'description': 'Find user id by email. If the user is not found, the function will return an error message.', 'parameters': {'type': 'object', 'properties': {'email': {'type': 'string', 'description': "The email of the user, such as 'something@example.com'."}}, 'required': ['email']}}}, {'type': 'function', 'function': {'name': 'find_user_id_by_name_zip', 'description': 'Find user id by first name, last name, and zip code. If the user is not found, the function will return an error message. By default, find user id by email, and only call this function if the user is not found by email or cannot remember email.', 'parameters': {'type': 'object', 'properties': {'first_name': {'type': 'string', 'description': "The first name of the customer, such as 'John'."}, 'last_name': {'type': 'string', 'description': "The last name of the customer, such as 'Doe'."}, 'zip': {'type': 'string', 'description': "The zip code of the customer, such as '12345'."}}, 'required': ['first_name', 'last_name', 'zip']}}}, {'type': 'function', 'function': {'name': 'get_order_details', 'description': 'Get the status and details of an order.', 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': "The order id, such as '#W0000000'. Be careful there is a '#' symbol at the beginning of the order id."}}, 'required': ['order_id']}}}, {'type': 'function', 'function': {'name': 'get_product_details', 'description': 'Get the inventory details of a product.', 'parameters': {'type': 'object', 'properties': {'product_id': {'type': 'string', 'description': "The product id, such as '6086499569'. Be careful the product id is different from the item id."}}, 'required': ['product_id']}}}, {'type': 'function', 'function': {'name': 'get_user_details', 'description': 'Get the details of a user, including their orders.', 'parameters': {'type': 'object', 'properties': {'user_id': {'type': 'string', 'description': "The user id, such as 'sara_doe_496'."}}, 'required': ['user_id']}}}, {'type': 'function', 'function': {'name': 'list_all_product_types', 'description': 'List the name and product id of all product types. Each product type has a variety of different items with unique item ids and options. There are only 50 product types in the store.', 'parameters': {'type': 'object', 'properties': {}, 'required': []}}}, {'type': 'function', 'function': {'name': 'modify_pending_order_address', 'description': 'Modify the shipping address of a pending order. The agent needs to explain the modification detail and ask for explicit user confirmation (yes/no) to proceed.', 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': "The order id, such as '#W0000000'. Be careful there is a '#' symbol at the beginning of the order id."}, 'address1': {'type': 'string', 'description': "The first line of the address, such as '123 Main St'."}, 'address2': {'type': 'string', 'description': "The second line of the address, such as 'Apt 1' or ''."}, 'city': {'type': 'string', 'description': "The city, such as 'San Francisco'."}, 'state': {'type': 'string', 'description': "The state, such as 'CA'."}, 'country': {'type': 'string', 'description': "The country, such as 'USA'."}, 'zip': {'type': 'string', 'description': "The zip code, such as '12345'."}}, 'required': ['order_id', 'address1', 'address2', 'city', 'state', 'country', 'zip']}}}, {'type': 'function', 'function': {'name': 'modify_pending_order_items', 'description': 'Modify items in a pending order to new items of the same product type. For a pending order, this function can only be called once. The agent needs to explain the exchange detail and ask for explicit user confirmation (yes/no) to proceed.', 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': "The order id, such as '#W0000000'. Be careful there is a '#' symbol at the beginning of the order id."}, 'item_ids': {'type': 'array', 'items': {'type': 'string'}, 'description': "The item ids to be modified, each such as '1008292230'. There could be duplicate items in the list."}, 'new_item_ids': {'type': 'array', 'items': {'type': 'string'}, 'description': "The item ids to be modified for, each such as '1008292230'. There could be duplicate items in the list. Each new item id should match the item id in the same position and be of the same product."}, 'payment_method_id': {'type': 'string', 'description': "The payment method id to pay or receive refund for the item price difference, such as 'gift_card_0000000' or 'credit_card_0000000'. These can be looked up from the user or order details."}}, 'required': ['order_id', 'item_ids', 'new_item_ids', 'payment_method_id']}}}, {'type': 'function', 'function': {'name': 'modify_pending_order_payment', 'description': 'Modify the payment method of a pending order. The agent needs to explain the modification detail and ask for explicit user confirmation (yes/no) to proceed.', 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': "The order id, such as '#W0000000'. Be careful there is a '#' symbol at the beginning of the order id."}, 'payment_method_id': {'type': 'string', 'description': "The payment method id to pay or receive refund for the item price difference, such as 'gift_card_0000000' or 'credit_card_0000000'. These can be looked up from the user or order details."}}, 'required': ['order_id', 'payment_method_id']}}}, {'type': 'function', 'function': {'name': 'modify_user_address', 'description': 'Modify the default address of a user. The agent needs to explain the modification detail and ask for explicit user confirmation (yes/no) to proceed.', 'parameters': {'type': 'object', 'properties': {'user_id': {'type': 'string', 'description': "The user id, such as 'sara_doe_496'."}, 'address1': {'type': 'string', 'description': "The first line of the address, such as '123 Main St'."}, 'address2': {'type': 'string', 'description': "The second line of the address, such as 'Apt 1' or ''."}, 'city': {'type': 'string', 'description': "The city, such as 'San Francisco'."}, 'state': {'type': 'string', 'description': "The state, such as 'CA'."}, 'country': {'type': 'string', 'description': "The country, such as 'USA'."}, 'zip': {'type': 'string', 'description': "The zip code, such as '12345'."}}, 'required': ['user_id', 'address1', 'address2', 'city', 'state', 'country', 'zip']}}}, {'type': 'function', 'function': {'name': 'return_delivered_order_items', 'description': "Return some items of a delivered order. The order status will be changed to 'return requested'. The agent needs to explain the return detail and ask for explicit user confirmation (yes/no) to proceed. The user will receive follow-up email for how and where to return the item.", 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': "The order id, such as '#W0000000'. Be careful there is a '#' symbol at the beginning of the order id."}, 'item_ids': {'type': 'array', 'items': {'type': 'string'}, 'description': "The item ids to be returned, each such as '1008292230'. There could be duplicate items in the list."}, 'payment_method_id': {'type': 'string', 'description': "The payment method id to pay or receive refund for the item price difference, such as 'gift_card_0000000' or 'credit_card_0000000'. These can be looked up from the user or order details."}}, 'required': ['order_id', 'item_ids', 'payment_method_id']}}}, {'type': 'function', 'function': {'name': 'think', 'description': 'Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.', 'parameters': {'type': 'object', 'properties': {'thought': {'type': 'string', 'description': 'A thought to think about.'}}, 'required': ['thought']}}}, {'type': 'function', 'function': {'name': 'transfer_to_human_agents', 'description': "Transfer the user to a human agent, with a summary of the user's issue. Only transfer if the user explicitly asks for a human agent, or if the user's issue cannot be resolved by the agent with the available tools.", 'parameters': {'type': 'object', 'properties': {'summary': {'type': 'string', 'description': "A summary of the user's issue."}}, 'required': ['summary']}}}]

def convert_trajectory_format(input_file, output_file):
    """
    Convert the expert trajectory file to the new format:
    [
      {
        "conversations": [
          {"from": "human", "value": "user instruction"},
          {"from": "function_call", "value": "tool arguments"},
          {"from": "observation", "value": "tool result"},
          {"from": "gpt", "value": "model response"}
        ],
        "system": "system prompt (optional)",
        "tools": "tool description (optional)"
      }
    ]
    """
    # Load the input file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Create the output structure
    output_data = []
    
    # Process each task - only use task_id and traj fields
    for task in data:
        task_id = task.get('task_id')
        traj = task.get('traj', [])
        
        # Initialize new format for this task
        new_task = {
            "conversations": [],
            "task_id": task_id  # Preserve task_id in the new format
        }
        
        # Track which tool names are used in this conversation
        used_tool_names = set()
        
        # Extract system message if present
        for message in traj:
            if message.get('role') == 'system':
                new_task["system"] = message.get('content', '')
                break
        
        # Track indices of messages to skip (non-existent tool calls and their observations)
        skip_indices = []
        
        # Convert the trajectory to the new format - one turn at a time
        for message in traj:
            role = message.get('role')
            content = message.get('content', '')
            
            # Skip system messages as they are handled separately
            if role == 'system':
                continue
                
            # User messages become "human", skip any message with ###STOP###
            elif role == 'user':
                if "###STOP###" in content:
                    continue
                    
                new_task["conversations"].append({
                    "from": "human",
                    "value": content
                })
            
            # Assistant messages with tool_calls field
            elif role == 'assistant' and message.get('tool_calls'):
                tool_calls = message.get('tool_calls', [])
                function_calls = []
                
                for idx, tool_call in enumerate(tool_calls):
                    if idx > 0:
                        print(f"Task {task_id} trajectory has multiple tool calls in one action. Skipped the others except the first one.")
                        continue
                    if tool_call.get('function'):
                        function_name = tool_call.get('function', {}).get('name', '')
                        arguments_str = tool_call.get('function', {}).get('arguments', '{}')
                        
                        # Add to used tool names
                        if function_name:
                            used_tool_names.add(function_name)
                        
                        try:
                            # Parse arguments as JSON
                            arguments = json.loads(arguments_str)
                            
                            function_calls.append({
                                "name": function_name,
                                "arguments": arguments
                            })
                        except json.JSONDecodeError:
                            print(f"Task {task_id} has a problematic function call that can't be parsed.")
                            print(f"arguments_str")
                            continue # if parsing fails
                            # If parsing fails, use the raw string
                            function_calls.append({
                                "name": function_name,
                                "arguments": arguments_str
                            })
                    
                # Convert the function calls to a string representation
                function_calls_str = json.dumps(function_calls[0]) # we actually want to make sure there is only one call in one turn
                
                new_task["conversations"].append({
                    "from": "function_call",
                    "value": function_calls_str
                })
            
            # Assistant messages with tool calls in content field (expert.json format)
            elif role == 'assistant' and message.get('content') and isinstance(message.get('content'), str):
                content = message.get('content', '')
                
                # Look for JSON array pattern in the content
                json_start = content.find('[{')
                json_end = content.rfind('}]')
                
                if json_start != -1 and json_end != -1 and json_end > json_start:
                    try:
                        # Extract just the JSON part
                        json_str = content[json_start:json_end + 2]
                        # Try to parse it as JSON to validate it's a proper function call
                        function_calls = json.loads(json_str)
                        
                        # Check if it's actually a valid function call structure
                        is_valid_function_call = True
                        for call in function_calls:
                            if isinstance(call, dict) and 'name' in call and 'arguments' in call:
                                # Add to used tool names
                                used_tool_names.add(call['name'])
                            else:
                                is_valid_function_call = False
                        # if len(function_calls) > 1:
                        #     print(task_id, "multi funciton_calls")
                        #     print(function_calls)
                        
                        if is_valid_function_call:
                            # Add function call to conversations (just the JSON part)
                            # This discards any thinking text that might be before the JSON
                            new_task["conversations"].append({
                                "from": "function_call",
                                "value": json_str
                            })
                            continue
                    except json.JSONDecodeError:
                        # If parsing fails, treat as a normal assistant message
                        pass
                
                # If we reached here, it's a normal assistant message
                new_task["conversations"].append({
                    "from": "gpt",
                    "value": content
                })
            
            # Normal assistant messages become "gpt"
            elif role == 'assistant':
                if message.get('content') is not None:  # Only add if content exists
                    new_task["conversations"].append({
                        "from": "gpt",
                        "value": message.get('content', '')
                    })
            
            # Tool messages become observations
            elif role == 'tool':
                tool_name = message.get('name')
                # Add tool name to the set of used tools
                if tool_name:
                    used_tool_names.add(tool_name)
                
                new_task["conversations"].append({
                    "from": "observation",
                    "value": message.get('content', '')
                })
        
        # Add tools information based on used tool names
        if used_tool_names:
            tools_for_task = []
            found_tools = set()
            
            # Find the tools in TOOL_INFO
            for tool in TOOL_INFO:
                if 'function' in tool and tool['function']['name'] in used_tool_names:
                    tools_for_task.append(tool)
                    found_tools.add(tool['function']['name'])
            
            # Check if all tools were found
            missing_tools = used_tool_names - found_tools
            if missing_tools:
                print(f"WARNING: Tools not found in TOOL_INFO: {missing_tools}")
                
                # Find and mark indices of function calls to missing tools and their corresponding observations
                i = 0
                while i < len(new_task['conversations']):
                    if new_task['conversations'][i]['from'] == 'function_call':
                        try:
                            function_calls = json.loads(new_task['conversations'][i]['value'])
                            # Check if this is a call to a missing tool
                            for call in function_calls:
                                if call.get('name') in missing_tools:
                                    # Mark this function call and the next observation to be skipped
                                    if i < len(new_task['conversations']) - 1 and new_task['conversations'][i+1]['from'] == 'observation':
                                        skip_indices.extend([i, i+1])
                        except json.JSONDecodeError:
                            pass
                    i += 1
            
            if tools_for_task:
                # Convert tools to string representation
                new_task["tools"] = json.dumps(tools_for_task)
        
        # Remove messages marked for skipping (non-existent tool calls and their observations)
        if skip_indices:
            # Sort in reverse order to avoid index shifting problems when removing items
            for idx in sorted(skip_indices, reverse=True):
                if idx < len(new_task['conversations']):
                    del new_task['conversations'][idx]
        
        # Check if the total number of turns is even after removing skipped messages
        if len(new_task['conversations']) % 2 == 0:
            # Add the converted task to the output
            output_data.append(new_task)
        else:
            # output_data.append(new_task)
            print(f"WARNING: Task {task_id} has an odd number of turns ({len(new_task['conversations'])}) since a transfer was called. Skipping this trajectory.")
            assert "Transfer successful" in new_task['conversations'][-1]['value']
    
    # Write the output file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    return output_data

def process_subset(input_file, output_file, limit=1):
    """Process only a subset of the tasks for testing purposes"""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    subset_data = data[:limit]
    
    # Create a new output file with just the subset data
    subset_output = output_file.replace('.json', '_subset.json') if output_file == input_file else output_file
    with open(subset_output, 'w') as f:
        json.dump(subset_data, f, indent=2)
    
    # Convert the subset to the new format
    return convert_trajectory_format(subset_output, output_file.replace('.json', '_converted.json'))

if __name__ == "__main__":
    import os
    import argparse
    
    # Default path to the input file
    default_input_file = 'data/expert.json'
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert trajectory format for tau-bench')
    parser.add_argument('input_file', nargs='?', default=default_input_file,
                        help='Path to the input JSON file (default: %(default)s)')
    parser.add_argument('output_file', nargs='?', 
                        help='Path to the output JSON file (default: input_filename_converted.json)')
    parser.add_argument('--subset', action='store_true',
                        help='Process only a subset of the data for testing')
    parser.add_argument('--limit', type=int, default=1,
                        help='Number of tasks to include in the subset (default: %(default)s)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set input file
    input_file = args.input_file
    
    # Set output file (default to input_filename_converted.json if not specified)
    if args.output_file:
        output_file = args.output_file
    else:
        output_file = os.path.splitext(input_file)[0] + '_converted.json'
    
    print("Input file: {}".format(input_file))
    print("Output file: {}".format(output_file))
    
    # Process subset or full dataset
    if args.subset:
        print("Processing subset of {} tasks".format(args.limit))
        subset_file = os.path.splitext(input_file)[0] + '_subset.json'
        process_subset(input_file, subset_file, limit=args.limit)
    else:
        print("Processing full dataset")
        convert_trajectory_format(input_file, output_file)
    
    print("Conversion complete!")