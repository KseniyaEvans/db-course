from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser
from pprint import pprint
from consolemenu import SelectionMenu

class bcolors:
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"

def cleanup():
    try:
        os.remove("../results/ukraine-is.xml")
        os.remove("../results/instrument_in_ua.xml")
        os.remove("../results/instrument_in_ua.xhtml")
    except OSError:
        pass

def show_start_menu():
    menu = SelectionMenu([
        'Crawl ukraine-is.com and instrument.in.ua',
        'Print all links crawled from ukraine-is.com',
        'Create XHTML table with products from instrument.in.ua'
    ], title="Select a task to do")
    menu.show()

    if menu.is_selected_item_exit():
        print('Bye!')
    else:
        index = menu.selected_option
        (crawl, print_all_links_from_ukraine_is, create_xhtml_table)[index]()

def press_enter(msg=''):
    return input(bcolors.CYAN + f'{msg}\nPress ENTER to continue...' + bcolors.RESET)

def crawl():
    process = CrawlerProcess(get_project_settings())
    process.crawl('ukraine-is')
    process.crawl('instrument_in_ua')
    process.start()

    press_enter('ukraine-is.com and instrument.in.ua were crawled, results are saved to .xml file.')
    show_start_menu()


def print_all_links_from_ukraine_is():
    root = etree.parse("../results/ukraine-is.xml")
    urls = root.xpath("//page")
    for page in urls:
        print(bcolors.GREEN + page.xpath("@url")[0])
    print(bcolors.RESET)
    press_enter()
    show_start_menu()

def create_xhtml_table():
    transform = etree.XSLT(etree.parse("transform.xsl"))
    result = transform(etree.parse("../results/instrument_in_ua.xml"))
    result.write("../results/instrument_in_ua.xhtml", pretty_print=True, encoding="UTF-8")
    webbrowser.get(using='safari').open('file://' + os.path.realpath("../results/instrument_in_ua.xhtml"))

    press_enter('XHTML table was created, results are saved.')
    show_start_menu()

if __name__ == '__main__':
    cleanup()
    show_start_menu()