import dircache

def get_data(ln):
    tmp = line.split('>')
    if len(tmp) == 2:
        return "0"
    else:
        val = str(tmp[1].split('<')[0]).lstrip('&nbsp;')
        #if float(val) < 0:
        #    val = "0"
        return val

def gethtml(lbl):
    try:
        val = t.split(lbl)[1].split("</td><td>")[3].lstrip('&nbsp;')
        if val == 'NaN':
            val = "-4"
        return val
    except:
        return "-4"

def getstumps(lbl):
    try:
        val = t.split("Stumps")[1].split(lbl)[1].split("</td><td>")[3].lstrip('&nbsp;')
        if val == 'NaN':
            val = "-4"
        return val
    except:
        return "-4"

xmlfolder  = "./xmls"
htmlfolder = "./htmls"
csv_file = "./FCCS_loadings_2.2_12-7-2010.csv"

csv = open(csv_file, 'w')

headers = ("fuelbed_number,site_name,site_description,ecoregion,cover_type," + 
           "overstory,midstory,understory,snags_C1Foliage,snags_C1Wood,snags_C1woFoliage,snags_C2,snags_C3,ladderFuels," +
           "shrubs_Primary,shrubs_Primary_perc_live,shrubs_Secondary,shrubs_Secondary_perc_live," +
           "nw_Primary,nw_Primary_perc_live,nw_Secondary,nw_Secondary_perc_live," +
           "w_Stump_Sound,w_Stump_Rotten,w_Stump_Lightered," +
           "litterDep,litterDep_perc,lichenDep,lichenDep_perc," + 
           "mossDep,mossDep_perc,mossType," +
           "litterShortNeedle_perc,litterLongNeedle_perc,litterOtherConf_perc,litterBroadLeafDecid_perc,litterBroadLeafEver_perc,litterPalmFrond_perc,litterGrass_perc," + 
           "g_DuffLoad_Total,g_DuffDep_Upper,g_DuffDep_Upper_perc,g_DuffDerivation_Upper," +
           "g_DuffDep_Lower,g_DuffDep_Lower_perc,g_DuffDerivation_Lower," +
           "g_BasDep,g_BasPercent,g_BasRadius,g_SMDepth,g_SMDensity,g_SMRadius," +
           "w_Sound_Sml_0_25,w_Sound_Sml,w_Sound_1_3,w_Sound_3_9,w_Sound_9_20,w_Sound_GT20," +
           "w_Rotten_3_9,w_Rotten_9_20,w_Rotten_GT20")



csv.write(headers)

xmls = dircache.listdir(xmlfolder)
htmls = dircache.listdir(htmlfolder)

for xml in xmls:
    if ".xml" in xml:
        if 'FCCS' in xml:
            fid = xml.split('_')[1][1:]
        if 'LF' in xml:
            fid = xml.split('_')[1]
        print "PROCESSING FCCS ID#: " + fid
        for html in htmls:
            hFID = html.rstrip(".tmp").rstrip('stratcat.html')
            
            if fid == hFID:

                # xml derived datas
                name = ""
                desc = ""
                eco = ""
                ct = ""
                
                sb_p_p = "0"
                sb_s_p = "0"

                nw_p_l = "0"
                nw_p_p = "0"
                nw_s_l = "0"
                nw_s_p = "0"

                llm = "0" # not pulled out or used by consume
                lit_d = "0"
                lit_p = "0"
                lit_a = "-4"
                
                lch_d = "0"
                lch_p = "0"
                mos_d = "0"
                mos_p = "0"
                mos_t = "0"

                pct_sn = "0"
                pct_ln = "0"
                pct_oc = "0"
                pct_bd = "0"
                pct_be = "0"
                pct_pf = "0"
                pct_gs = "0"

                df = "0" # not pulled out or used by consume
                dfu_d = "0"
                dfu_p = "0"
                dfu_v = "0"
                dfl_d = "0"
                dfl_p = "0"
                dfl_v = "0"

                bas_d = "0"
                bas_p = "0"
                bas_r = "0"
                
                sqm_d = "0"
                sqm_n = "0"
                sqm_r = "0"

                w_sml1 = "0"
                w_sml2 = "0"
                w_1_3 = "0"
                w_3_9 = "0"
                w_9_20 = "0"
                w_G20 = "0"
                w_3_9r = "0"
                w_9_20r = "0"
                w_G20r = "0"

                # html derived datas
                c_over = "0"
                c_mid = "0"
                c_under = "0"
                c_sg1f = "0"
                c_sg1w = "0"
                c_sg1o = "0"
                c_sg2 = "0"
                c_sg3 = "0"
                c_lad = "0"

                sbp = "0"
                sbs = "0"

                stp_s = "0"
                stp_r = "0"
                stp_l = "0"


                text = open(xmlfolder + "/" + xml)
                lines = text.readlines()
                text.close()

                text = open(htmlfolder + "/" + html)
                hlines = text.readlines()
                text.close()
                

                # Get xml data
                for line in lines:
                    # header info
                    if '<site_name>' in line:
                        name = line.split('>')[1].split('<')[0]
                    
                    if '<site_description>' in line:
                        desc = line.split('>')[1].split('<')[0].replace(',','~')
                    
                    if 'label="ecoregion"' in line:
                        eco = line.split('>')[1].split('<')[0].replace(',','~')
                        
                    if 'label="cover_type"' in line:
                        ct = line.split('>')[1].split('<')[0].replace(',','~')
  
                    # shrubbies
                    if 'shrubs.shrub.primary_layer.percent_live.mode' in line:
                        sb_p_p = get_data(line)
                    if 'shrubs.shrub.secondary_layer.percent_live.mode' in line:
                        sb_s_p = get_data(line)

                    # non-woodies
                    if 'non_woody_fuels.primary_layer.percent_live.mode' in line:
                        nw_p_p = get_data(line)
                    if 'non_woody_fuels.primary_layer.loading.mode' in line:
                        nw_p_l = get_data(line)
                    if 'non_woody_fuels.secondary_layer.loading.mode' in line:
                        nw_s_l = get_data(line)
                    if 'non_woody_fuels.secondary_layer.percent_live.mode' in line:
                        nw_s_p = get_data(line)

                    # llmies
                    if 'moss_lichen_litter.litter.depth.mode' in line:
                        lit_d = get_data(line)
                    if 'moss_lichen_litter.litter.percent_cover.mode' in line:
                        lit_p = get_data(line)
                    if 'moss_lichen_litter.ground_lichen.depth.mode' in line:
                        lch_d = get_data(line)
                    if 'moss_lichen_litter.ground_lichen.percent_cover.mode' in line:
                        lch_p = get_data(line)
                    if 'moss_lichen_litter.moss.depth.mode' in line:
                        mos_d = get_data(line)
                    if 'moss_lichen_litter.moss.percent_cover.mode' in line:
                        mos_p = get_data(line)
                    if 'moss_lichen_litter.moss.type' in line:
                        mos_t = get_data(line)

                    # litter distribution
                    if 'short_needle_pine.relative_cover"/>' in line:
                        pct_sn = get_data(line)
                    if 'long_needle_pine.relative_cover"/>' in line:
                        pct_ln = get_data(line)
                    if 'other_conifer.relative_cover"/>' in line:
                        pct_oc = get_data(line)
                    if 'broadleaf_deciduous.relative_cover"' in line:
                        pct_bd = get_data(line)
                    if 'broadleaf_evergreen.relative_cover"' in line:
                        pct_be = get_data(line)
                    if '.palm_frond.relative_cover' in line:
                        pct_pf = get_data(line)
                    if 'litter_type.grass.relative_cover' in line:
                        pct_gs = get_data(line)

                    # duffers
                    if 'ground_fuel.duff.upper.depth.mode' in line:
                        dfu_d = get_data(line)
                    if 'ground_fuel.duff.upper.percent_cover.mode' in line:
                        dfu_p = get_data(line)
                    if 'ground_fuel.duff.upper.derivation' in line:
                        dfu_v = get_data(line)
                    if 'ground_fuel.duff.lower.depth.mode' in line:
                        dfl_d = get_data(line)
                    if 'ground_fuel.duff.lower.percent_cover.mode' in line:
                        dfl_p = get_data(line)
                    if 'ground_fuel.duff.lower.derivation' in line:
                        dfl_v = get_data(line)

                    # basal. accumulate.
                    if 'ground_fuel.basal_accumulation.depth.mode' in line:
                        bas_d = get_data(line)
                    if 'ground_fuel.basal_accumulation.percent_affected.mode' in line:
                        bas_p = get_data(line)
                    if 'ground_fuel.basal_accumulation.radius.mode' in line:
                        bas_r = get_data(line)

                    # SQUIRRELS!!!!
                    if 'ground_fuel.squirrel_middens.depth.mode' in line:
                        sqm_d = get_data(line)
                    if 'ground_fuel.squirrel_middens.number_per_unit_area.mode' in line:
                        sqm_n = get_data(line)
                    if 'ground_fuel.squirrel_middens.radius.mode' in line:
                        sqm_r = get_data(line)

                    # woodies
                    if 'loadings_zero_to_three_inches.zero_to_quarter_inch.mode' in line:
                        w_sml1 = get_data(line)
                    if 'loadings_zero_to_three_inches.quarter_inch_to_one_inch.mode' in line:
                        w_sml2 = get_data(line)
                    if 'loadings_zero_to_three_inches.one_to_three_inches.mode' in line:
                        w_1_3 = get_data(line)

                    if 'sound_wood.loadings_greater_than_three_inches.three_to_nine_inches.mode' in line:
                        w_3_9 = get_data(line)
                    if 'sound_wood.loadings_greater_than_three_inches.nine_to_twenty_inches.mode' in line:
                        w_9_20 = get_data(line)
                    if 'sound_wood.loadings_greater_than_three_inches.greater_than_twenty_inches.mode' in line:
                        w_G20 = get_data(line)

                    if 'rotten_wood.loadings_greater_than_three_inches.three_to_nine_inches.mode' in line:
                        w_3_9r = get_data(line)
                    if 'rotten_wood.loadings_greater_than_three_inches.nine_to_twenty_inches.mode' in line:
                        w_9_20r = get_data(line)
                    if 'rotten_wood.loadings_greater_than_three_inches.greater_than_twenty_inches.mode' in line:
                        w_G20r = get_data(line)


                # Get html data
                t = hlines[0]
                c_over = gethtml(">Overstory")
                c_mid = gethtml(">Midstory")
                c_under = gethtml(">Understory")
                
                c_sg1f = gethtml(">Class 1 foliage")
                c_sg1w = gethtml(">Class 1 wood")
                c_sg1o = gethtml(">Class 1 other")
                c_sg2 = gethtml(">Class 2")
                c_sg3 = gethtml(">Class 3")
                c_lad = gethtml(">Ladder fuels")

                sbp = t.split(">Shrubs")[1].split("</td><td>")[15].lstrip('&nbsp;')
                sbs = t.split(">Shrubs")[1].split("</td><td>")[25].lstrip('&nbsp;')

                stp_s = getstumps(">Sound wood")
                stp_r = getstumps(">Rotten wood")
                stp_l = getstumps(">Lightered")

                ls = [fid,name,desc,eco,ct,c_over,c_mid,c_under,c_sg1f,c_sg1w,c_sg1o,
                      c_sg2,c_sg3,c_lad,sbp,sb_p_p,sbs,sb_s_p,nw_p_l,nw_p_p,nw_s_l,nw_s_p,
                      stp_s,stp_r,stp_l,lit_d,lit_p,lch_d,lch_p,mos_d,mos_p,mos_t,
                      pct_sn,pct_ln,pct_oc,pct_bd,pct_be,pct_pf,pct_gs,
                      df,dfu_d,dfu_p,dfu_v,dfl_d,dfl_p,dfl_v,bas_d,
                      bas_p,bas_r,sqm_d,sqm_n,sqm_r,
                      w_sml1,w_sml2,w_1_3, w_3_9,w_9_20,w_G20,w_3_9r,
                      w_9_20r,w_G20r,]

                sl = ','.join(ls)
                csv.write("\n" + sl)

          
                