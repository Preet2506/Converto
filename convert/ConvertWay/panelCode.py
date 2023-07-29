from io import BytesIO
import pandas as pd
# import openpyxl
from . import config
from datetime import datetime, timedelta
import os
from django.http import HttpResponse,FileResponse
from dateutil.relativedelta import relativedelta


# funtion to load file
def load(file,sheet="Sheet1"):
    df = pd.read_excel(file)
    return df

# funtion to add invoice date
def addInvoice(name,courier,df):
    df = df
    # Get the last date of the current month
    today = datetime.today()- relativedelta(months=1)
    last_day = datetime(today.year, today.month, 1) + timedelta(days=32)
    last_day = last_day.replace(day=1) - timedelta(days=1)
    invoice_date_str = last_day.strftime("%Y-%m-%d")

    # Add the last date of the current month to a new column
    df["invoice_date"] = invoice_date_str

    # getting the month name
    month_name = (datetime.today()- relativedelta(months=1)).strftime("%b")
    year = datetime.now().strftime("%y")
    df["invoice_number"] = f'{courier}{month_name}{year}'

    # Save the updated dataframe to a new Excel file
    # df.to_excel(name, index=False)
    return df



# funtion to copy the data from given file to our common file
def convert(name,format , col,courier,df):

    # Load the Excel files
    print('pass 4/8')
    df1 = df
    # filepath = os.path.abspath("Common.xlsx")
    df2 = load('/home/django/combine/Combine/Common.xlsx')

    # Rearrange the columns
    df1 = df1.rename(columns=format)

    # Drop empty rows and reset the index
    df1 = df1.dropna(how='all').reset_index(drop=True)
    df2 = df2.dropna(how='all').reset_index(drop=True)

    # Combine the dataframes
    columns_to_copy = col

    df_combined = pd.concat([df2, df1[columns_to_copy]], ignore_index=True)

    # Create a file-like buffer to receive Excel data.
    buffer = BytesIO()

    # Write the DataFrame to the buffer.
    # df_combined.to_excel(buffer, index=False)
    df = df_combined
    print('5/8')
    df = addInvoice(buffer,courier,df_combined)
    # addInvoiceNo(buffer,courier)
    print('6/8')
    # if (courier == 'ATS'):
    #     df = dropATS(buffer, df_combined)
    # Set the filename with the courier name and current timestamp.

    print('7/8')
    df.to_excel(buffer,index=False)
    print('7.5')
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    filename = f"{courier}_{timestamp}.xlsx"

    # Generate the response.
    response = HttpResponse(buffer.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    # adding invoice date to the file
    print('8/8')
    formatted_time = datetime.now().strftime("%H:%M:%S")
    print("Current time:", formatted_time)
    return response


# funtion to convert weight from kgs to grams
def weight(df,column):
    # df = pd.read_excel(name)
    # Multiply the values in a specific column by 100, starting from the second row
    df[column] = df[column] * 1000
    # Save the updated dataframe to a new Excel file
    return df


# funtion to apply condition of rto of ats
def rtoATS(row):
    if row["Leg Type"] == "REVERSE":
        row["return_tracking_number"] = row["Tracking Id"]
        return row["return_tracking_number"]
    elif row["Leg Type"] == "FORWARD":
        row["return_tracking_number"] = ""
        return row["return_tracking_number"]

# funtion to apply conditions of zone of ats
def zoneATS(row):
    if row["Zone"] == "Local":
        row["Zone"] = 1
        return row["Zone"]
    elif row["Zone"] == "Regional":
        row["Zone"] = 2
        return row["Zone"]
    elif row["Zone"] == "Metro":
        row["Zone"] = 3
        return row["Zone"]
    elif row["Zone"] == "Remote":
        row["Zone"] = 4
        return row["Zone"]
    elif row["Zone"] == "National":
        row["Zone"] = 5
        return row["Zone"]

# function to copy the data of a ats file
def ats(name,courier):
    # calling mapping and column names to be copied from the given file from the config file
    formatted_time = datetime.now().strftime("%H:%M:%S")
    print("Current time:", formatted_time)
    print("pass 1/8")
    ats1 = config.atsmap
    col = config.atscol

    # Load the Excel file
    df = load(name)
    if "FWD Awb_no" in df.columns:
        print("The column exists.")
    else:
        return "error"
    print('pass 1.5/8')

    # droping duplicates
    df = df[df['Charge Type'] == 'Total']

    df = weight(df,"Billable Weight (in KG)")
    # creating a rto column for the rows which are eligible
    df["return_tracking_number"] = df.apply(rtoATS, axis=1)
    # df.to_excel(name, index=False)
    print('pass 2/8')
    # handling zones of the ats file
    df["Zone"] = df.apply(zoneATS,axis=1)
    print('pass 3/8')
    # df.to_excel(name, index=False)
    # Calling the funtion to copy the data
    response = convert(name,ats1,col,courier,df)

    return response


def rtoBD(row):
    if str(row["CAWBNO"]).endswith("R"):
        row["return_tracking_number"] = row["CAWBNO"]
        return row["return_tracking_number"]
    else :
        row["return_tracking_number"] = ""
        return row["return_tracking_number"]


def bd(name,courier):
    bd1 = config.bdmap
    col = config.bdcol

    df = load(name)

    if "CAWBNO" in df.columns:
        print("The column exists.")
    else:
        return "error"

    df = weight(df ,"NCHRGWT")
    df["return_tracking_number"] = df.apply(rtoBD, axis=1)
    # df.to_excel(name, index=False)

    df["tax_amount"] = df["NTOTALAMT"]*0.18
    df["total_amount"] = df["NTOTALAMT"] + df["tax_amount"]
    # df.to_excel(name, index=False)
    response = convert(name, bd1, col, courier,df)

    return response

def rtoDLV(row):
    if row["status"] == "RTO":
        row["return_tracking_number"] = row["waybill_num"]
        return row["return_tracking_number"]
    elif row["status"] == "Delivered":
        row["return_tracking_number"] = ""
        return row["return_tracking_number"]

def zoneDLV(row):
    if row["zone"] == "A":
        row["Zone"] = 1
        return row["Zone"]
    elif row["zone"] == "B":
        row["Zone"] = 2
        return row["Zone"]
    elif row["zone"] == "C":
        row["Zone"] = 3
        return row["Zone"]
    elif row["zone"] == "E":
        row["Zone"] = 4
        return row["Zone"]
    elif row["zone"] == "D":
        row["Zone"] = 5
        return row["Zone"]

# dlv courier
def dlv(name, courier):
    dlv1 = config.dlvmap
    col = config.dlvcol

    df = load(name)

    if "waybill_num" in df.columns:
        print("correct file")
    else:
        return "error"

    # rto condition
    df["return_tracking_number"] = df.apply(rtoDLV, axis=1)

    # zone condition
    df["Zone"] = df.apply(zoneDLV,axis=1)

    # add taxes
    df["CGST"] = df["CGST"]+df["SGST/UGST"]+df["IGST"]
    response = convert(name, dlv1, col, courier, df)

    return response

def rtoDTDC(row):
    if row["RTO"] != 0:
        row["return_tracking_number"] = row["FWD_NO"]
        return row["return_tracking_number"]
    else:
        row["return_tracking_number"] = ""
        return row["return_tracking_number"]

def zoneDTDC(row):
    if row["ZONEING"] == "LOCAL":
        row["Zone"] = 1
        return row["Zone"]
    elif row["ZONEING"] == "WITHINSTATE" or row["ZONEING"] =="WITHINZONE":
        row["Zone"] = 2
        return row["Zone"]
    elif row["ZONEING"] == "METRO":
        row["Zone"] = 3
        return row["Zone"]
    elif row["ZONEING"] == "SPL":
        row["Zone"] = 4
        return row["Zone"]
    elif row["ZONEING"] == "ROIA" or  row["ZONEING"] == "ROIB":
        row["Zone"] = 5
        return row["Zone"]

def dtdc(name, courier):
    dtdc1 = config.dtdcmap
    col = config.dtdccol

    df = load(name)

    if "CONSIGN_WT" in df.columns:
        print("correct file")
    else:
        return "error"

    # if weight in kgs
    weight(df,"CONSIGN_WT")

    # rto condition
    df["return_tracking_number"] = df.apply(rtoDTDC, axis=1)

    # zone condition
    df["Zone"] = df.apply(zoneDTDC,axis=1)

    response = convert(name, dtdc1, col, courier, df)

    return response

def rtoECOM(row):
    if row["Parent/RTS AWB"] > 0:
        temp = row["Parent/RTS AWB"]
        row["New Return Tracking Number"] = row["airwaybill_number"]
        row["New Airwaybill Number"] = temp
    else:
        row["New Return Tracking Number"] = ""
        row["New Airwaybill Number"] = row["airwaybill_number"]
    return row

def zoneECOM(row):
    if row["Billable Zone / Rate"] == "Intra-city":
        row["Zone"] = 1
        return row["Zone"]
    elif row["Billable Zone / Rate"] == "Within Zones" or row["Billable Zone / Rate"] =="Within Zones -ROS" or row["Billable Zone / Rate"] =="Within Zones -UP":
        row["Zone"] = 2
        return row["Zone"]
    elif row["Billable Zone / Rate"] == "METRO":
        row["Zone"] = 3
        return row["Zone"]
    elif row["Billable Zone / Rate"] == "NORTH EAST" or row["Billable Zone / Rate"] == "NORTH EAST -ROS" or row["Billable Zone / Rate"] == "NORTH EAST -UP":
        row["Zone"] = 4
        return row["Zone"]
    elif row["Billable Zone / Rate"] == "Rest of India" or  row["Billable Zone / Rate"] == "Rest of India -ROS" or row["Billable Zone / Rate"] == "Rest of India -UP":
        row["Zone"] = 5
        return row["Zone"]


def ecom(name, courier):
    ecom1 = config.ecommap
    col = config.ecomcol

    df = load(name)

    if "airwaybill_number" in df.columns:
        print("correct file")
    else:
        return "error"

    # if weight in kgs
    weight(df,"chargeable_weight")

    # rto condition
    df = df.apply(rtoECOM, axis=1)
    df = df.drop(["airwaybill_number", "Parent/RTS AWB"], axis=1)
    df = df.rename(columns={"New Airwaybill Number": "airwaybill_number", "New Return Tracking Number": "return_tracking_number"})

    # zone condition
    df["Zone"] = df.apply(zoneECOM,axis=1)

    # if taxes and total need to be added
    df["tax_amount"] = df["Total"] * 0.18
    df["total_amount"] = df["Total"] + df["tax_amount"]

    response = convert(name, ecom1, col, courier, df)

    return response

def rtoEKART(row):
    if row["accrual_ref_4"] == "rto":
        row["return_tracking_number"] = row["tracking_id"]
        return row["return_tracking_number"]
    elif row["accrual_ref_4"] == "forward":
        row["return_tracking_number"] = ""
        return row["return_tracking_number"]

def zoneEKART(row):
    if row["zone_type"] == "within_city":
        row["Zone"] = 1
        return row["Zone"]
    elif row["zone_type"] == "within_region":
        row["Zone"] = 2
        return row["Zone"]
    elif row["zone_type"] == "metro_std":
        row["Zone"] = 3
        return row["Zone"]
    elif row["zone_type"] == "NE_JK_std":
        row["Zone"] = 4
        return row["Zone"]
    elif row["zone_type"] == "ROI_std":
        row["Zone"] = 5
        return row["Zone"]

def ekart(name, courier):
    ekart1 = config.ekartmap
    col = config.ekartcol

    df = load(name)

    if "tracking_id" in df.columns:
        print("correct file")
    else:
        return "error"

    # rto condition
    df["return_tracking_number"] = df.apply(rtoEKART, axis=1)

    # zone condition
    df["Zone"] = df.apply(zoneEKART,axis=1)

    response = convert(name, ekart1, col, courier, df)

    return response

def rtoSMARTR(row):
    if row["FWD/RTO"] == "RTO AWB":
        row["return_tracking_number"] = row["AWBNumber"]
        return row["return_tracking_number"]
    elif row["FWD/RTO"] == "FWD":
        row["return_tracking_number"] = ""
        return row["return_tracking_number"]

def zoneSMARTR(row):
    if row["Zone"] == "within City":
        row["zone"] = 1
        return row["zone"]
    elif row["Zone"] == "within Region":
        row["zone"] = 2
        return row["zone"]
    elif row["Zone"] == "Metro to Metro":
        row["zone"] = 3
        return row["zone"]
    elif row["Zone"] == "North East":
        row["zone"] = 4
        return row["zone"]
    elif row["Zone"] == "Rest of India":
        row["zone"] = 5
        return row["zone"]

def smartr(name, courier):
    smartr1 = config.smartrmap
    col = config.smartrcol

    df = load(name)

    if "AWBNumber" in df.columns:
        print("correct file")
    else:
        return "error"

    # changing awb number
    df["AWBNumber"] = df["AWBNumber"].apply(lambda x: f"XSE{x}001")

    # if weight in kgs
    weight(df,"ChargedWeight")
    # rto condition
    df["return_tracking_number"] = df.apply(rtoSMARTR, axis=1)

    # zone condition
    df["zone"] = df.apply(zoneSMARTR,axis=1)

    # if taxes and total need to be added
    df["IGST"] = df["IGST"] + df["SGST"] + df["CGST"]

    response = convert(name, smartr1, col, courier, df)

    return response

def rtoXB(row):
    if row["Shipment Status"] == "Rto":
        row["return_tracking_number"] = row["AWB Number"]
        return row["return_tracking_number"]
    elif row["Shipment Status"] == "Delivered":
        row["return_tracking_number"] = ""
        return row["return_tracking_number"]

def zoneXB(row):
    if row["Zone"] == "z1":
        row["zone"] = 1
        return row["zone"]
    elif row["Zone"] == "z2":
        row["zone"] = 2
        return row["zone"]
    elif row["Zone"] == "z3":
        row["zone"] = 3
        return row["zone"]
    elif row["Zone"] == "z5":
        row["zone"] = 4
        return row["zone"]
    else:
        row["zone"] = 5
        return row["zone"]


def xb(name, courier):
    xb1 = config.xbmap
    col = config.xbcol

    df = load(name)

    if "AWB Number" in df.columns:
        print("correct file")
    else:
        return "error"

    # if weight in kgs
    weight(df,"Charged Weight")
    # rto condition
    df["return_tracking_number"] = df.apply(rtoXB, axis=1)

    # zone condition
    df["zone"] = df.apply(zoneXB,axis=1)

    # if taxes and total need to be added
    df["Freight Charges"] = df["Freight Charges"]+df["COD Charges"]
    df["IGST"] = df["IGST"] + df["SGST"] + df["CGST"]


    response = convert(name, xb1, col, courier, df)

    return response

# funtion to clear the already existing data in our output file
# def clearOp():
#     if (os.path.exists('/home/shipway/Django/combine/output.xlsx')):
#         df = load('/home/shipway/Django/combine/output.xlsx')
#
#         # Clear the data in the dataframe
#         df = pd.DataFrame(columns=df.columns)
#         print("cleared")
#         df.to_excel('/home/shipway/Django/combine/output.xlsx', index=False)

