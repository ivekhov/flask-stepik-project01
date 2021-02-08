from flask import Flask, render_template, redirect, url_for, abort
import data


app = Flask(__name__)
tours = data.tours
departures = data.departures


@app.route('/')
def main():
    try:
        return render_template('index.html', tours=tours)
    except:
        return render_not_found()


@app.route('/departures/<departure>/')
def show_deparutes(departure):
    try:
        city = departures[departure]
        count = 0
        min_price = 0
        max_price = 0
        min_nights = 0
        max_nights = 0
        hotels_idxs = []
        for idx, tour in tours.items():
            if tour["departure"] == departure:
                hotels_idxs.append(idx)
                count += 1
                if min_price == 0:
                    min_price = tour["price"]
                elif min_price > tour["price"]:
                    min_price = tour["price"]
                if max_price < tour["price"]:
                    max_price = tour["price"]

                if min_nights == 0:
                    min_nights = tour["nights"]
                elif min_nights > tour["nights"]:
                    min_nights = tour["nights"]
                if max_nights < tour["nights"]:
                    max_nights = tour["nights"]

        return render_template('departure.html', city=city, count=count, min_price=min_price,
                               max_price=max_price, min_nights=min_nights, max_nights=max_nights,
                               hotels_idxs=hotels_idxs, tours=tours)
    except:
        return render_not_found()


@app.route('/tours/<id>/')
def show_tours(id):
    try:
        tour = tours[int(id)]
        return render_template('tour.html', tours=tours, idx=int(id),
                               departures=departures)
    except:
        return render_not_found()


@app.route('/data')
def show_all():
    response = '<h1>Все туры:</h1>'
    for id in data.tours.keys():
        item = data.tours[id]
        response += f'<p>{item["country"]}: <a href="/data/tours/{id}">{item["title"]} & {item["price"]} {item["stars"]} </a></p>'
    return response


@app.route('/data/departures/<departure>')
def show_direction(departure):
    try:
        response = f'<h1>Туры по направлению {data.cities[departure]}:</h1>'
        for id in data.tours.keys():
            item = data.tours[id]
            if item['departure'] == departure:
                response += f'<p>{item["country"]}: <a href="/data/tours/{id}">{item["title"]} & {item["price"]} {item["stars"]} </a></p>'
    except:
        return render_not_found()
    return response


@app.route('/data/tours/<tour_id>')
def show_tour(tour_id):
    try:
        item = data.tours[int(tour_id)]
        response = f'<h1>{item["country"]}: {item["title"]} {item["price"]}:</h1>'
        response += f'<p>{item["nights"]} ночей</p>'
        response += f'<p>{item["price"]} рублей</p>'
        response += f'<p>{item["description"]}</p>'
    except:
        return render_not_found()
    return response


@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим:\n{}".format(error), 500


@app.errorhandler(404)
def render_not_found():
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 5000)
