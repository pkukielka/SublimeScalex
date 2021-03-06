import sublime, sublime_plugin
import urllib.request, urllib.error
import os.path
import webbrowser
import threading
import json

class SublimeScalexCommand(sublime_plugin.WindowCommand):

  def run(self):
    view = self.window.show_input_panel(
      'Find function:',
      SublimeScalexHistory.current(),
      self.__queryScalex,
      None,
      None)
    self.__setSyntax(view, 'SublimeScalex.hidden-tmLanguage')
    view.settings().set('is_widget', True)
    view.settings().set('gutter', False)
    view.settings().set('rulers', [])

  def __setSyntax(self, view, file_name):
    path = lambda package_name: 'Packages{0}{1}{0}{2}'.format(os.sep, package_name, file_name)

    if os.path.isfile(os.path.join(sublime.packages_path(), "SublimeScalex")):
      view.set_syntax_file(path('SublimeScalex'))
    else:
      view.set_syntax_file(path('Scalex Documentation Search'))

  def __queryScalex(self, query_string):
    SublimeScalexHistory.add(query_string)
    settings = sublime.load_settings('SublimeScalex.sublime-settings')
    queryThread = QueryScalex(
      settings.get('scalex_api_url'),
      settings.get('scaladoc_url'),
      query_string,
      self.__displayRecords,
      settings.get('scalex_api_timeout'),
      settings.get('results_limit'))
    queryThread.start()

  def __displayRecords(self, records, urls):
    self.urls = urls
    sublime.active_window().show_quick_panel(records, self.__openInBrowser)

  def __openInBrowser(self, index):
    if (index >= 0):
      webbrowser.open_new_tab(self.urls[index])


class SublimeScalexHistory(sublime_plugin.TextCommand):
  index = 0
  history = ['']

  @classmethod
  def current(cls):
    return cls.history[cls.index]

  @classmethod
  def add(cls, new_query):
    if cls.history[-1] != new_query:
      cls.history.append(new_query)
      cls.index = len(cls.history) - 1

  def run(self, edit, backwards=False):
    self.index += -1 if backwards else 1
    if self.index == len(self.history) or self.index < -len(self.history):
      self.index = -1 if backwards else 0

    self.view.erase(edit, sublime.Region(0, self.view.size()))
    self.view.insert(edit, 0, self.history[self.index])


class QueryScalex(threading.Thread):
  def __init__(self, scalex_url, scaladoc_url, query_string, response_callback, timeout, limit):
    self.limit = limit
    self.timeout = timeout
    self.scalex_url = scalex_url
    self.scaladoc_url = scaladoc_url
    self.query_string = query_string
    self.response_callback = response_callback
    threading.Thread.__init__(self)

  def run(self):
    try:
      url = "%s?%s" % (self.scalex_url, urllib.parse.urlencode({'q': self.query_string, 'per_page': self.limit}))
      http_file = urllib.request.urlopen(url, timeout=self.timeout)
      response = json.loads(http_file.read().decode('utf8'), strict=False)
      self.response_callback(self.__prepareRecordsList(response), self.__prepareUrlsList(response))
      http_file.close()
    except urllib.error.HTTPError as e:
      sublime.status_message('%s: HTTP error %s contacting Scalex API' % (__name__, str(e.code)))
    except urllib.error.URLError as e:
      sublime.status_message('%s: URL error %s contacting Scalex API' % (__name__, str(e.reason)))
    return

  def __prepareRecordsList(self, json_response):
    return [[self.__parseSignature(record),
            self.__parsePackage(record),
            self.__parseComment(record)]
            for record in json_response['results']]

  def __prepareUrlsList(self, json_response):
    return [self.scaladoc_url + '#' + self.__parsePackage(record)
            for record in json_response['results']]

  def __parseComment(self, record):
    try: return record['comment']['short']['txt']
    except KeyError: return ''

  def __parseSignature(self, record):
    try: return 'def ' + record['name'] + record['typeParams'] + record['valueParams'] + ': ' + record['resultType']
    except KeyError: return ''

  def __parsePackage(self, record):
    try: return record['parent']['qualifiedName']
    except KeyError: return ''