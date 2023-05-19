from models import Quote
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

while True:
    command = input("Введіть команду: ")

    if command.startswith("name:") or command.startswith("tag:"):
        # Перевірка кешу Redis
        if redis_client.exists(command):
            cached_result = redis_client.get(command)
            print(cached_result.decode('utf-8'))
        else:
            if command.startswith("name:"):
                search_term = command.split(":")[1].strip()
                authors = Author.objects(fullname__icontains=search_term)
                quotes = Quote.objects(author__in=authors)
            elif command.startswith("tag:"):
                search_term = command.split(":")[1].strip()
                quotes = Quote.objects(tags__icontains=search_term)
            
            result = []
            for quote in quotes:
                result.append(quote.quote)
                print(quote.quote)
            
            redis_client.set(command, '\n'.join(result))
    elif command == "exit":
        break
    else:
        print("Невідома команда!")
