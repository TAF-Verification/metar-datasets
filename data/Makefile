YEAR=2024
FOLDER=raw
STATION=mroc
GET-METARS=get-metars

download: jan feb mar apr may jun jul aug sep oct nov dec
	@echo $(YEAR) data for station $(STATION) downloaded succesfully
	@rm metar.txt

jan:
	@echo Downloading data for january-$(YEAR)
	$(GET-METARS) -i $(YEAR)-01-01 -f $(YEAR)-01-31T23:59:00 -o $(STATION)
	cat metar.txt > $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

feb:
	@echo Downloading data for february-$(YEAR)
	$(GET-METARS) -i $(YEAR)-02-01 -f $(YEAR)-02-28T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

mar:
	@echo Downloading data for march-$(YEAR)
	$(GET-METARS) -i $(YEAR)-03-01 -f $(YEAR)-03-31T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

apr:
	@echo Downloading data for april-$(YEAR)
	$(GET-METARS) -i $(YEAR)-04-01 -f $(YEAR)-04-30T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

may:
	@echo Downloading data for may-$(YEAR)
	$(GET-METARS) -i $(YEAR)-05-01 -f $(YEAR)-05-31T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

jun:
	@echo Downloading data for june-$(YEAR)
	$(GET-METARS) -i $(YEAR)-06-01 -f $(YEAR)-06-30T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

jul:
	@echo Downloading data for july-$(YEAR)
	$(GET-METARS) -i $(YEAR)-07-01 -f $(YEAR)-07-31T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

aug:
	@echo Downloading data for august-$(YEAR)
	$(GET-METARS) -i $(YEAR)-08-01 -f $(YEAR)-08-31T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

sep:
	@echo Downloading data for september-$(YEAR)
	$(GET-METARS) -i $(YEAR)-09-01 -f $(YEAR)-09-30T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

oct:
	@echo Downloading data for october-$(YEAR)
	$(GET-METARS) -i $(YEAR)-10-01 -f $(YEAR)-10-31T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

nov:
	@echo Downloading data for november-$(YEAR)
	$(GET-METARS) -i $(YEAR)-11-01 -f $(YEAR)-11-30T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20

dec:
	@echo Downloading data for december-$(YEAR)
	$(GET-METARS) -i $(YEAR)-12-01 -f $(YEAR)-12-31T23:59:00 -o $(STATION)
	cat metar.txt >> $(FOLDER)/$(STATION)/$(YEAR).txt
	@sleep 20