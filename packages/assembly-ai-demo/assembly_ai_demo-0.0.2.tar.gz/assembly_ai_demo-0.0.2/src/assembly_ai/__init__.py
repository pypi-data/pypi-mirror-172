from random import randint

EMOJIES = ['😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', 
'🙃', '😊', '😇', '🥰', '😍', '😘', '😚', '😙', '🥲', '😋', '😛', '😜']

def hello_emoji(name: str='') -> str:
  return f'Hello {name}{EMOJIES[randint(0, 20)]}!'

def get_emoji(n=1):
  

if __name__ == '__main__':
  print(hello_emoji())
  print(hello_emoji('Afiz'))