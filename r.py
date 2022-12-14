# REGEX
date_re = r"(?<=PickUp: \(\b[a-zA-Z]{3}\b\)) [0-9]{2}-\b[a-zA-Z]{3}\b"
time_re = r"(?<=PickUp: \(\b[a-zA-Z]{3}\b\) [0-9]{2}-\b[a-zA-Z]{3}\b) \d{1,2}:\d{2}"
flight_re = r"(?<=Flt#:)([A-Za-z0-9_-]+|)"
pick_re = r"[\n\r].*PickUp:\s*([^\n\r]*)(?=\s+(Arrive|Depart))(?<=\S)"
drop_re = r"[\n\r].*Drop Off:\s*([^\n\r]*)(?=\s+@)(?<=\S)"
name_re = r"(?<![0-9]{4}\n)(?<=\n)([0-9]+|-[0-9]+)\s*(.+?(?=F\/A|CAP|F\/O))|(Trip#)"  # Group 2
crewID_re = r"(?<![0-9]{4}\n)(?<=\n)([0-9]+|-[0-9]+)\s*(.+?(?=F\/A|CAP|F\/O))|(Trip#)"  # Group 1
trip_re = r"(?<=-- Total --\n)([0-9]+)"
pax_re = r"(\d+)(?=\s*(?=\$\d+(?:\.\d+)?))"
status_re = r"(?<![0-9]{4}\n)(?<=\n)([0-9]+|-[0-9]+)\s*(.+?(?=F\/A|CAP|F\/O))(F\/A|CAP|F\/O|)\s*.*(\*\* Cancelled \*\*| Previously CF'ed| Updated)|(Trip#)" # Group 4
drr_re = r"(.*\s(?=\(FLL time\)))"

# FLL
hilton_fll_re = r"Hilton to FLL"
fll_hilton_re = r"FLL to Hilton"
fll_sheratonFll_re = r"FLL to Sheraton FLL"
sheratonFll_fll_re = r"Sheraton FLL to FLL"
fll_hyatt_re = r"FLL to Hyatt Place FLL"
hyatt_fll_re = r"Hyatt Place FLL to FLL"
wyndham_fll_re = r"Wyndham Garden FLL to FLL"
fll_wyndham_re = r"FLL to Wyndham Garden FLL"
# MCO
hotel_mco_re = r"Hotel to MCO"
mco_hotel_re = r"MCO to Hotel"
element_mco_re = r"Element Orlando to MCO"
mco_element_re = r"MCO to Element Orlando"
sheratonMco_mco_re = r"Sheraton Orlando to MCO"
mco_sheratonMco_re = r"MCO to Sheraton Orlando"
dtMco_mco_re = r"DoubleTree MCO Airport to MCO"
mco_dtMco_re = r"MCO to DoubleTree MCO Airport"
dtSeaworld_mco_re = r"DoubleTree MCO at SeaWorld to MCO"
mco_dtSeaworld_re = r"MCO to DoubleTree MCO at SeaWorld"
mco_fairfield_re = r"MCO to Fairfield Inn MCO Airport"
fairfield_mco_re = r"Fairfield Inn MCO Airport to MCO"
crowne_mco_re = r"Crowne Plaza Universal to MCO"
mco_crowne_re = r"MCO to Crowne Plaza Universal"
# TPA
embassy_tpa_re = r"Embassy to TPA"
tpa_embassy_re = r"TPA to Embassy"
tpaPlaza_tpa_re = r"Renaissance Tampa Plaza to TPA"
tpa_tpaPlaza_re = r"TPA to Renaissance Tampa Plaza"
tpa_courtyard_re = r"TPA to Courtyard by Marriott Tampa"
courtyard_tpa_re = r"Courtyard by Marriott Tampa to TPA"
ac_tpa_re = r"AC Hotel Airport to TPA"
tpa_ac_re = r"TPA to AC Hotel Airport"
hyattTPA_tpa = r"Hyatt Place Tampa Airport/ Westshore to TPA"
tpa_hyattTPA = r"TP to Hyatt Place Tampa Airport/ Westshore"
# MIA
inter_mia_re = r"Inter to MIA"
mia_inter_re = r"MIA to Inter"
hamptonMia_mia_re = r"Hampton Inn Miami Airport West to MIA"
mia_hamptonMia_re = r"MIA to Hampton Inn Miami Airport West"
eb_mia_re = r"EB Hotel to MIA"
mia_eb_re = r"MIA to EB Hotel"
