# telus-bulk-types-pypi

## Import models using

    from telus_bulk.models

## E.g
    from telus_bulk.models.worker_job import AddressProcessingJob
    job_data: AddressProcessingJob = AddressProcessingJob.parse_raw(message.data)

## PYTEST
The .env file must have the PYTHONPATH variable  

    PYTHONPATH=src

# Changelog

1.1.9:
- CheckServiceQualification and CheckServiceQualificationItem models updated with createdAt field
- OverAllProcessStatus, OverAllProcess, OverAllData classes created

1.1.8:
- Pagination model validated for page to always be greater than 1  
- CheckServiceQualificationItem:  
        effective_qualification_item_date  create as str  
        expiration_date updated from datetime to str  
- ServiceRefOrValue  
    service_specification updated to Union of List[ServiceSpecificationRef] | List[ServiceSpecification]

1.1.6:
- PageDto paginationMetadata -> meta

1.1.6:
- Added pagination models and pytest

1.1.5:
- Added RelatedParty class to CityCoverageProcessedJob.relatedParty, instead of a string array
- WebMethods init module updated to export get and post methods
- 645/service/place updated priority to match first PlaceAMS class

1.1.3:
- Added Web Methods

1.1.0:
- Added more AMS fields to PlaceAMS, First demo ready!

1.0.7:
- Added more AMS fields to PlaceAMS

1.0.6:
- Partner list bug fix

1.0.5:
- Added supported partners enum and list  

1.0.3:
- Optional AMS Coordinates object fields, except for latitude and longitude

1.0.2:
- Added CityCoverageProcessedJob class
- CSQI service supports a PlaceAms as Place