from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond

def is_first_request(data:RedcapResponseFirst):
    details = data.details if isinstance(data.details, dict) else data.details.to_dict()
    mr_request = details.get("mr_request")
    mr_request_dt = details.get("mr_request_dt")
    mr_request_dt_2 = details.get("mr_request_dt_2")
    return mr_request and mr_request_dt and not mr_request_dt_2

def is_second_request(data:RedcapResponseFirst):
    details = data.details if isinstance(data.details, dict) else data.details.to_dict()
    mr_request = details.get("mr_request")
    mr_request_dt = details.get("mr_request_dt")
    mr_request_dt_2 = details.get("mr_request_dt_2")
    mr_received = details.get("mr_received")
    return mr_request and mr_request_dt and mr_request_dt_2 and mr_received in ("0", "")

def is_second_request_partial(data:RedcapResponseFirst):
    details = data.details if isinstance(data.details, dict) else data.details.to_dict()
    mr_request = details.get("mr_request")
    mr_request_dt = details.get("mr_request_dt")
    mr_request_dt_2 = details.get("mr_request_dt_2")
    mr_received = details.get("mr_received")
    mr_rec_all = details.get("mr_rec_all")
    return mr_request and mr_request_dt and mr_request_dt_2 and mr_received and mr_rec_all in ("0", "")