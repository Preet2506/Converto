atsmap = {"FWD Awb_no" : "tracking_number" , "Billable Weight (in KG)" : "billed_weight" , "Tax Exclusive Charge Value (INR)" : "base_price" , "Tax Amount (INR)" : "tax_amount" , "Tax Inclusive Charge Value (INR)" : "total_amount" , "Zone" : "zone_id"}

atscol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount'	,'total_amount','zone_id']

bdmap = {"CAWBNO" : "tracking_number" , "NCHRGWT" : "billed_weight" , "NTOTALAMT" : "base_price"  }

bdcol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount','total_amount']

dlvmap = {'waybill_num':'tracking_number','charged_weight':'billed_weight','gross_amount':'base_price','CGST':'tax_amount','total_amount':'total_amount' , "Zone" : "zone_id"}

dlvcol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount'	,'total_amount','zone_id']

dtdcmap = {'FWD_NO':'tracking_number','CONSIGN_WT':'billed_weight','GROSS':'base_price','GST':'tax_amount','NET':'total_amount' , "Zone" : "zone_id"}

dtdccol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount'	,'total_amount','zone_id']

ecommap = {'airwaybill_number':'tracking_number','chargeable_weight':'billed_weight','Total':'base_price' , "Zone" : "zone_id"}

ecomcol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount'	,'total_amount','zone_id']

ekartmap = {'tracking_id':'tracking_number','ceil_weight':'billed_weight','total_revenue':'base_price' ,'total_tax':'tax_amount','value_including_tax':'total_amount', "Zone" : "zone_id"}

ekartcol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount'	,'total_amount','zone_id']

smartrmap = {'AWBNumber':'tracking_number','ChargedWeight':'billed_weight','Revenue':'base_price' ,'IGST':'tax_amount','Invoice Total':'total_amount', "zone" : "zone_id"}

smartrcol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount','total_amount','zone_id']

xbmap = {'AWB Number':'tracking_number','Charged Weight':'billed_weight','Freight Charges':'base_price' ,'IGST':'tax_amount','Grand Total':'total_amount', "zone" : "zone_id"}

xbcol = ['tracking_number','return_tracking_number','billed_weight','base_price','tax_amount','total_amount','zone_id']
