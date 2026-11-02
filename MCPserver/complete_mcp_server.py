#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from fastmcp import FastMCP

mcp=FastMCP(
    name="First Server"
)

print("MCP Server created successfully!")

@mcp.tool
def add(a:int,b:int)-> int:
    """ this can accept two numbers and return the sum of those numbers """
    return a+b

@mcp.tool
def mul(a:int,b:int=1):
    """ this can accept two numbers and return the multiplication of those numbers """
    return a*b



# ### Connect with FastMCP Client

# In[39]:


from fastmcp import Client

async with Client(mcp) as client:
    print("protocall version",client.protocol_version)
    tools= await client.list_tools()
    print("print the tool")
    result= await client.call_tool("add",{"a":12,"b":3})
    print(result.data)


# ### All about the Mcp Tools- Context / Tasks / Auth

# In[ ]:


from fastmcp import FastMCP, Client
import json


async def show(server: FastMCP, tool_name: str):
    async with Client(server) as client:
        tools = await client.list_tools()
        tool = None
        for t in tools:
            if t.name == tool_name:
                tool = t
                break

        if tool is None:
            print(f"Tool '{tool_name}' not found.")
            return

        print(f"Name: {tool.name}")
        print(f"Description: {tool.description}")
        print(json.dumps(tool.inputSchema, indent=2))


# In[49]:


await show(mcp,"mul")


# In[53]:


from typing import Literal

@mcp.tool
async def export(table:str,format:Literal["csv","excel","json"]="csv"):
    """Export a table data into specific format"""
    return "Export done"


# In[54]:


await show(mcp,"export")


# ### A Pydantic model as an argument

# In[58]:


from pydantic import BaseModel, Field


class Shipment(BaseModel):
    order_id: str = Field(description="This is order id placed by the user...")
    quantity: int
    express: bool = False


@mcp.tool
def book_shipment(shipment: Shipment) -> dict:
    """Book a shipment for an order"""
    return {"booked": shipment.order_id, "qty": shipment.quantity}


# In[59]:


await show(mcp,"book_shipment")


# Exception / Error Handeling

# In[ ]:


from fastmcp.exceptions import ToolError

@mcp.tool
def new_charges_amount(amount:float):
    "Charge on a Card"
    if amount < 100:
        raise ToolError("Amount value should not be less then 100 rs.")
    return "Charges done..."


# In[76]:


async with Client(mcp) as client:
    res=await client.call_tool("new_charges_amount",{"amount":20},raise_on_error=False)
    print(res)


# #### `Context` - Talking back to the client while server is running..

# In[81]:


from fastmcp import FastMCP,Context
import asyncio
ctxserver=FastMCP("cts-demo")

@ctxserver.tool
async def send_mails(emails:list[str],context: Context)->str:
    """Send Emails to many student at a time"""
    totalStudents=len(emails)
    ### one email at a time, 2 sec to complete
    for i in range(totalStudents):
        email=emails[i]
        await context.report_progress(progress=i+1,total=totalStudents,message=f"Sending email to :{email}")
        await asyncio.sleep(2)
    return "Email Sent to all the student"
        


# In[82]:


async def watch_email_process(progess,total,message):
    print(message)

async with Client(ctxserver) as client:
    res=await client.call_tool("send_mails",{"emails":["prateek","nikhil","ajay"]},progress_handler=watch_email_process)
    print(res)
    
    
    

