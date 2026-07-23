from services.runtime import kernel


def get_health_prediction(asset_id, horizon_days=14):

    readings = kernel.state.get_history(
        asset_id
    )


    current_health = kernel.health.calculate_health(
        readings
    )


    historical = calculate_history(
        readings
    )


    prediction = predict_degradation(
        current_health,
        horizon_days
    )


    failure_probability = calculate_failure_probability(
        current_health
    )


    return {

        "health": round(
            current_health
        ),

        "rul": calculate_rul(
            current_health
        ),

        "failure_probability": f"{failure_probability}%",

        "confidence": calculate_confidence(
            readings
        ),

        "historical": {
            "Historical health": historical
        },

        "predicted": {
            "Predicted health": prediction,
            "Intervention threshold":
                [70] * len(prediction)
        },

        "telemetry": format_telemetry(
            readings
        )
    }



def calculate_history(readings):

    history = []

    for i in range(len(readings)):

        health = kernel.health.calculate_health(
            readings[:i+1]
        )

        history.append(
            round(health,1)
        )

    return history



def predict_degradation(
    current,
    days
):

    prediction = []

    health = current


    for _ in range(days):

        health -= 0.5

        prediction.append(
            round(
                max(0, health),
                1
            )
        )

    return prediction



def calculate_failure_probability(
    health
):

    risk = 100 - health

    return min(
        100,
        round(risk)
    )



def calculate_rul(
    health
):

    if health > 90:
        return "90+ days"

    if health > 75:
        return "45 days"

    if health > 50:
        return "14 days"

    return "<7 days"



def calculate_confidence(
    readings
):

    if len(readings) > 20:
        return "90%"

    if len(readings) > 5:
        return "75%"

    return "Low"



def format_telemetry(readings):

    data = []

    for reading in readings[-10:]:

        data.append(
            {
                "Sensor": reading.sensor_type.value,

                "Observed": reading.value,

                "Time": reading.timestamp.strftime(
                    "%H:%M:%S"
                )
            }
        )

    return data