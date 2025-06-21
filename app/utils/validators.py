from models.redcap_response_first import RedcapResponseFirst


def is_first_request(data: RedcapResponseFirst) -> bool:
    """
    Real-Time: Trigger if First Request is made and no second request yet.
    Conditions:
    - mr_request == "1"
    - mr_request_dt is not null
    - mr_request_dt_2 is null
    """
    details = data.details if isinstance(data.details, dict) else data.details.to_dict()
    return (
        details.get("mr_request") == "1"
        and bool(details.get("mr_request_dt"))
        and not details.get("mr_request_dt_2")
    )


def is_second_request_manual_not_received(data: RedcapResponseFirst) -> bool:
    """
    Real-Time: Second request explicitly triggered but records not received.
    Conditions:
    - mr_request_2 == "1"
    - mr_request_dt_2 is not null
    - mr_received == "0" or empty
    """
    details = data.details if isinstance(data.details, dict) else data.details.to_dict()
    return (
        details.get("mr_request_2") == "1"
        and bool(details.get("mr_request_dt_2"))
        and details.get("mr_received") in ("0", "", None)
    )


def is_second_request_partial_received(data: RedcapResponseFirst) -> bool:
    """
    Real-Time: Second request done, some records received but not all.
    Conditions:
    - mr_request_2 == "1"
    - mr_request_dt_2 is not null
    - mr_received == "1" (some received)
    - mr_rec_all == "0" or empty (not all received)
    """
    details = data.details if isinstance(data.details, dict) else data.details.to_dict()
    return (
        details.get("mr_request_2") == "1"
        and bool(details.get("mr_request_dt_2"))
        and details.get("mr_received") == "1"
        and details.get("mr_rec_all") in ("0", "", None)
    )
