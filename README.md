SublimeScalex
=============

## Introduction

This plugin provides integration between Sublime Text and [Scalex](http://scalex.org/).  
It allows you to search for any Scala or Scalaz function directly from ST.  
Quoting Scalex main page:

##### Names and Types
Searches can be either textual (a list of words), or by type (a type signature) or both.
A search is considered a text search unless it contains a combination of text and symbols, or if it starts with `:`.
To search for both a type and a name, place a `:` between them, for example size: `List[A] => Int`.

##### Example queries

* `map` Search for the text `map`
* `list map` Search for the text `list` and the text `map`
* `list[a] => (a => boolean) => list[a]` Search for the type `List[A] => (A => Boolean) => List[A]`
* `: list[a] => a` Search for the type `List[A] => A`
* `conserve: List[a] => (a => b) => List[b]` Search for the text `conserve` and the type `List[A] => (A => B) => List[B]`

##### Packages
You can reduce the search scope to one or more packages:

* `foldl +scala` Search `foldl` only in `scala`
* `foldl +scalaz` Search `foldl` only in `scalaz`
* `foldl -scalaz` Search `foldl` everywhere except in `scalaz`

## Installation
Right now SublimeScalex works only under ST3 (or at least was not tested under ST2 yet).
If there will be enough interest I'll port it to older version as well.

The easiest way to install SublimeScalex is to use [Package Control](https://sublime.wbond.net/packages/Scalex%20Documentation%20Search).
You can also install it from here, by downloading and copying this folder to your packages directory.

## Usage
Open the Command Palette and search for 'SublimeScalex' or just hit `Ctrl + Alt + F` to open **Function search** bar:

![alt text](http://oi40.tinypic.com/23k7rit.jpg "Screenshot 1")

Describe what you are looking for as explained in the **Introduction** section and hit Enter.
You will see list filled with entries matching your query. You can filter it further using standard Sublime fuzzy search.

![alt text](http://oi43.tinypic.com/119t0z9.jpg "Screenshot 2")

If you want to see more details about any entry highlight it and hit Enter again (or just click it with the mouse).
You will be moved to appropriate scaladoc, if it exists.  
If you down want to open scaladoc just hit Esc.

Default number of showed results is limited to 20 to speed up querying, but you can change it in settings if you like.

## Final notes
For bigger Scala projects I still prefer to use IntelliJ, but for simple scripts and snippets I found Sublime to be more pleasant.
If you want to turn your Sublime into powerful Scala development environment then I recommend you to look at few more plugins:

* [sublime-ensime](https://github.com/sublimescala/sublime-ensime) - error checking with Scala presentation compiler, and more
* [SublimeREPL](https://github.com/wuub/SublimeREPL) - Scala REPL inside Sublime, let you play with your code in more interactive way
* [LoadFileToRepl](https://github.com/laughedelic/LoadFileToRepl) - load current file into REPL, very comfortable to use
