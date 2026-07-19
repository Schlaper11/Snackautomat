try:
    from machine import I2C, Pin
except ImportError:  # Lokaler Test ohne Pico-Hardware
    I2C = None

    class Pin:  # type: ignore[override]
        OUT = 1
        IN = 0
        PULL_UP = 2

        def __init__(self, pin_id, mode=None, pull=None):
            self.pin_id = pin_id
            self._value = 1

        def value(self, new_value=None):
            if new_value is None:
                return self._value
            self._value = new_value


PRODUCTS = {
    1: ("Cola", 150),
}

COIN_VALUE_CENTS = 50
MOTOR_PIN = 15
COIN_PIN = 14


def format_price(cents):
    euros = cents // 100
    rest = cents % 100
    return f"{euros},{rest:02d} €"


def show_message(message):
    print(message)


def run_motor(motor_pin):
    show_message("Motor läuft... Ausgabe startet.")
    motor_pin.value(1)
    sleep_ms(2000)
    motor_pin.value(0)


def sleep_ms(ms):
    try:
        import time

        time.sleep_ms(ms)  # MicroPython
    except AttributeError:
        import time

        time.sleep(ms / 1000)  # CPython fallback


def wait_for_payment(target_cents, coin_pin):
    paid = 0
    show_message(f"Bitte {format_price(target_cents)} einwerfen")

    while paid < target_cents:
        if I2C is None:
            try:
                inserted = int(input("Eingeworfene Cent (z.B. 50): "))
            except EOFError:
                show_message("Eingabe beendet.")
                return paid
            except ValueError:
                show_message("Ungültiger Betrag.")
                continue
            paid += inserted
            show_message(f"Eingezahlt: {format_price(paid)}")
            continue

        if coin_pin.value() == 0:
            paid += COIN_VALUE_CENTS
            show_message(f"Münze erkannt: +{COIN_VALUE_CENTS} Cent")
            show_message(f"Eingezahlt: {format_price(paid)}")
            sleep_ms(300)

    return paid


def main():
    motor = Pin(MOTOR_PIN, Pin.OUT)
    motor.value(0)

    coin_input = Pin(COIN_PIN, Pin.IN, Pin.PULL_UP)

    while True:
        try:
            selection = int(input("Produktnummer eingeben (1 = Cola): "))
        except EOFError:
            show_message("Programm beendet.")
            break
        except ValueError:
            show_message("Bitte nur Zahlen eingeben.")
            continue

        if selection not in PRODUCTS:
            show_message("Produkt nicht vorhanden.")
            continue

        name, price = PRODUCTS[selection]
        show_message(f"{name} kostet {format_price(price)}")

        paid = wait_for_payment(price, coin_input)
        if paid < price:
            show_message("Zahlung abgebrochen.")
            continue
        show_message("Betrag vollständig. Produkt wird ausgegeben.")
        run_motor(motor)


if __name__ == "__main__":
    main()
