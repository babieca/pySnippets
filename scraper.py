#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# #!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import requests
import os
import re       # regex
import uuid     # for unique id
import xml.etree.ElementTree as ET
import random
import time
import mmap     # to find string in file
import tldextract       # Accurately separate the TLD from the registered domain andsubdomains of a URL, using the Public Suffix List.
from  threading import Thread, Lock
from multiprocessing.pool import ThreadPool
from multiprocessing import Queue
from datetime import datetime
from urlparse import urlparse
from bs4 import BeautifulSoup


TARGETS = [
    'http://127.0.0.1',]

PROC = 1
THRDS = 1
MAX_DEPTH = 1
SLEEP = False
SLEEP_MIN = 1
SLEEP_MAX = 3

PATH = os.getcwd()
LOGPATH = 'logs'
EXCLUDED_URIS = "no_scrap_uris.txt"
USER_AGENT = 'useragentswitcher.xml'
LOGSUBFOLDER = 'tmp'
LOGALL = 'logall.txt'
LOGURLS = 'logurls.txt'
LOGDOMAINS = 'logdomains.txt'
LOGSKIP = 'logskip.txt'
LOGERR = 'logerr.txt'


LOGPATH = LOGPATH + datetime.utcnow().strftime('_%Y-%m-%d_%H-%M-%S')
lock = Lock()


def get_request(uri):
    class Object(object):
            pass

    errobj = Object()
    errobj.status_code = -1
    errobj.url = ''

    try:
        checkSSL = False
        if checkSSL:
            proto = get_protocol(uri)
            if proto == 'https':
                return errobj
        headers = {
                'Connection': 'close',
                'User-Agent': get_user_agent()}
        response = requests.get(uri, headers=headers, verify=checkSSL, stream=False, timeout=10)

        if not response.status_code:
            return errobj

        if response.encoding is None:
            response.encoding = 'utf-8'

        return response

    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        return errobj
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        return errobj
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        return errobj


def is_ascii(s):
    try:
        s.decode('ascii')
    except Exception as e:
        return False
    else:
        return True


def get_user_agent():
    lst = []
    f_useragent = os.path.join(PATH, USER_AGENT)
    if os.path.isfile(f_useragent):
        tree = ET.parse(f_useragent)
        root = tree.getroot()
        for node in root.iter('useragent'):
            ua = node.get('useragent')
            if ua: lst.append(ua)

    result = None
    if len(lst):
        while not result:
            result = random.choice(lst)
    else:
        result = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2869.0 Safari/537.36"

    return result


def is_valid_uri(uri):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.match(uri):
        return True
    return False


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def get_protocol(uri):
    if is_valid_uri(uri):
        parsed_uri = urlparse(uri)
        proto = '{uri.scheme}'.format(uri=parsed_uri)
        return proto
    return False


def get_index_list_dict(list_of_dict, key):
    try:
        idx = next(index for (index, d) in enumerate(list_of_dict) if d["uri"] == key)
        return idx
    except Exception as e:
        return -1


def deleteContent(pathf):
    if not os.path.dirname(pathf):
        pathf = os.path.join(PATH, pathf)
    if os.path.isabs(pathf):
        open(pathf, 'w').close()
        return True
    return False


def writeHeader(pathf):
    if not os.path.dirname(pathf):
        pathf = os.path.join(PATH, pathf)
    if os.path.isfile(pathf):
        sttime = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
        f = open(pathf,'a')
        f.write('#'*100 + '\n')
        f.write('Scan started on ' + sttime + '\n')
        f.write('#'*100 + '\n')
        f.close()
        return True
    return False


def writeFile(pathf, line):
    if not os.path.dirname(pathf):
        pathf = os.path.join(PATH, pathf)

    if os.path.isfile(pathf):
        lock.acquire()  # thread blocks at this line until it can obtain lock

        f = open(pathf,'a')
        f.write(line)
        f.flush()
        f.close()

        lock.release()

        return True

    return False


def log2console(text):
    lock.acquire()
    print(text)
    sys.stdout.flush()
    lock.release()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def is_str_in_file(pathf, str_to_search):
    if not os.path.dirname(pathf):
        pathf = os.path.join(PATH, pathf)
    if os.path.isfile(pathf):
        f = open(pathf)
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find(str_to_search) != -1:
            return True
    return False


def skip_uri_with_format(uri):
    pattern = "(?i)\.(bmp|png|gif|jpe?g|pdf|msi|zip|rar|zvd|exe|xlsx?|docx?|pptx?|PrestoObra)$"
    prog = re.compile(pattern)
    if prog.search(uri):
        return True
    pattern = "(?i)^(javascript|mailto|skype):.*"
    prog = re.compile(pattern)
    if prog.search(uri):
        return True
    pattern = "\s"
    prog = re.compile(pattern)
    if prog.search(uri):
        return True
    return False


def webscraping(pinfo):

    logdir = pinfo['logdir']
    logerr = os.path.join(logdir, LOGERR)
    logskip = os.path.join(logdir, LOGSKIP)

    try:
        uri = pinfo['uri'].encode('utf-8').strip()
    except Exception as e:
        writeFile(logerr, uri + "| Reason: encode(\'utf-8\')\n")
        return

    print "original:   " + uri

    sts = pinfo['status']
    if not isinstance(sts, int):
        writeFile(logerr, uri + "| Reason: not isinstance(status, int)\n")
        return

    if sts == 404:
        writeFile(logerr, uri + "| Reason: 404 status code\n")
        return

    pid = pinfo['uuid']
    program = re.compile('(?i)^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$')
    if  program.match(str(pid).encode('utf-8')) is None:
        writeFile(logerr, uri + "| Reason: not valid UUID(v4)\n")
        return

    depth = pinfo['depth'] + 1
    if not isinstance(depth, int):
        writeFile(logerr, uri + "| Reason: not isinstance(depth, int)\n")
        return

    if not is_valid_uri(uri):
        writeFile(logerr, uri + "| Reason: not is_valid_uri(uri)\n")
        return

    in_root = False
    domain = re.search('^([a-z][a-z0-9+\-.]*:(//[^/?#]+)?)?', uri).group(0)  # http://www.google.co.uk
    for t in TARGETS:
        tdom = re.search('^([a-z][a-z0-9+\-.]*:(//[^/?#]+)?)?', t).group(0)
        if tdom == domain:
            in_root = True
            break

    # scrape all the links in a root or in other with a limit of MAX_DEPTH
    if (depth > MAX_DEPTH) and (not in_root):
        return

    if skip_uri_with_format(uri):
        writeFile(logskip, uri + "| Reason: skip_uri_with_format(uri)\n")
        return

    response = get_request(uri)

    if response.status_code < 0:
        writeFile(logerr, uri + "| Reason: not response.status_code\n")
        return

    if response.history:
        try:
            uri = response.url.encode('utf-8').strip()  # in case there was a redirection
            response = get_request(uri)                 # get request of final destination if found a redirect
        except Exception as e:
            writeFile(logerr, uri + "| Reason: redirection encode(\'utf-8\')\n")
            return

    print "redirect?:   " + uri

    print response.headers['Content-Type']
    if 'text/html' not in response.headers['Content-Type']:
        writeFile(logskip, uri + "| Reason: \'Content-Type\'] != \'text/html\'\n")
        return

    try:
        soup = BeautifulSoup(response.content, "lxml")
    except Exception as e:
        writeFile(logerr, uri + "| Reason: BeautifulSoup()\n")
        return

    domain_pid = re.search('^([a-z][a-z0-9+\-.]*:(//[^/?#]+)?)?', uri).group(0)  # http://www.google.co.uk

    pinfo['uri'] = uri          # overwritte original uri incase there was a redirect
    pinfo['status'] = response.status_code
    pinfo['time'] = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
    pinfo['domain'] = domain_pid

    links = set()
    for x in soup.find_all('img'):
        t = x.get('src')
        if t is None or t == uri or t == '#':
            continue
        try:
            links.add(t.encode('utf-8').strip())
        except Exception as e:
            continue
    for x in soup.find_all('a'):
        t = x.get('href')
        if t is None or t == uri or t == '#':
            continue
        try:
            links.add(t.encode('utf-8').strip())
        except Exception as e:
            continue

    if len(links) == 0:
        return

    # Split the list of links in blocks of size(THRDS)
    ch = chunks(list(links), THRDS)
    lst = []
    for m in ch:
        items = run_parallel_in_threads(analyse_links, zip(m), depth, pid, domain_pid, logdir)
        for i in range(0, len(items)):
            # check if items is multidimensional list
            if isinstance(items[0], list):
                for j in range(0, len(items[i])):
                    lst.append(items[i][j])
                    pinfo['child'].append(items[i][j]['uri'])
            else:
                lst.append(items[i])
                pinfo['child'].append(items[i]['uri'])
        # Sleep, to prevent DOS
        if SLEEP:
            time.sleep(random.randint(SLEEP_MIN,SLEEP_MAX))

    # empty the list
    result = []
    for res in lst:
        if res is not None:
            tm = res['time']
            status = res['status']
            uri = res['uri'].encode('utf-8').strip()
            uriorg = res['uri_original'].encode('utf-8').strip()
            depth = res['depth']
            uid = res['uuid']
            pid = res['pid']
            child = res['child']
            domain = res['domain']
            fldr = res['logdir']

            logtmp = os.path.join(fldr, LOGALL)
            writeFile(logtmp, "%s|%03d|%s|%s|%03d|%s|%s|%s|%s\n" %
                      (tm, status, uri, uriorg, depth, domain, uid, pid, ','.join(child)))

            logtmp = os.path.join(fldr, LOGDOMAINS)
            if not is_str_in_file(logtmp, domain):
                writeFile(logtmp, domain + '\n')

            result.append(res)

    return result


def analyse_links(links, depth, pid, domain_pid, logdir):

    result = []

    logurls = os.path.join(logdir, LOGURLS)
    logskip = os.path.join(logdir, LOGSKIP)
    excf = os.path.join(PATH, EXCLUDED_URIS)

    for li in links:

        log2console("[starting...] " + li)
        pattern = "(?i)^(javascript|mailto|skype):.*"
        prog = re.compile(pattern)
        if prog.search(li):
            writeFile(logskip, li + "| Reason: (?i)^(javascript|mailto|skype):.*\n")
            log2console("   [semicolon...] " + li)
            continue
        pattern = "\s"
        prog = re.compile(pattern)
        if prog.search(li):
            writeFile(logskip, li + "| Reason: \'spaces\'\n")
            log2console("   [spaces...] " + li)
            continue
        pattern = "^#.*$"
        prog = re.compile(pattern)
        if prog.search(li):
            writeFile(logskip, li + "| Reason: \'#\'\n")
            log2console("   [#...] " + li)
            continue

        pattern1 = r'(?i)^\/[^\/]+.*$'              # if it starts with single / but not more
        pattern2 = r'(?i)^\/\/[^\/]+.*$'            # if it starts with double // but not more or single
        pattern3 = r'(?i)^www\..*$'
        pattern4 = r'(?i)^(https?|ftps?)://.*$'
        p1 = re.compile(pattern1)
        p2 = re.compile(pattern2)
        p3 = re.compile(pattern3)
        p4 = re.compile(pattern4)
        if p1.match(li):        # starts with a single '/'
            li = domain_pid + li
        elif p2.match(li):      # starts with a double '//'
            pass
        elif p3.match(li):      # starts with 'www.'
            li = 'http://' + li
        elif not p4.match(li):
            li = domain_pid + '/' + li

        # replace all '//' with '/' but not if after http://...
        li = re.sub(u"(?<!(?<=http:)|(?<=https:)|(?<=ftp:)|(?<=ftps:))\/\/", "/", li)

        if not is_valid_uri(li):
            writeFile(logerr, li + "| Reason: not is_valid_uri(li)\n")
            log2console("   [invalid...] " + li)
            continue

        # check if I have already skipped it
        if is_str_in_file(logskip, li):
            log2console("   [logskip...] " + li)
            continue

        # from http://forums.bbc.co.uk'
        # ext.registered_domain: 'bbc.co.uk'
        # (ext.subdomain, ext.domain, ext.suffix)
        # ('forums', 'bbc', 'co.uk')
        ext = tldextract.extract(li)
        if skip_uri_with_format(li):        # Register but skip
            writeFile(logerr, li + "| Reason: skip_uri_with_format(li)\n")
            log2console("   [format...] " + li)
            continue

        if is_str_in_file(logurls, li) or is_str_in_file(excf, ext.registered_domain):
            log2console("   [registered...] " + li)
            continue                        # Register

        k = uuid.uuid4()
        r = get_request(li)
        domain_li = re.match('^([a-z][a-z0-9+\-.]*:(//[^/?#]+)?)?', li).group(0)        # http://www.google.co.uk
        result.append({
            'time': datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3],
            'status': r.status_code if r.status_code else -1,
            'uri': r.url,
            'uri_original': li,
            'depth': depth,
            'uuid': k,
            'pid': pid,
            'child': [],
            'domain': domain_li,
            'logdir': logdir})
        writeFile(logurls, li + '\n')
        log2console("   [ok...] " + li)

    return result


def run_parallel_in_threads(target, args_list, arg1=None, arg2=None, arg3=None, arg4=None):

    items = []
    q = Queue()

    # wrapper to collect return value in a Queue
    def task_wrapper(*args):
        q.put(target(*args))
    threads = [Thread(target=task_wrapper, args=(args, arg1, arg2, arg3, arg4)) for args in args_list]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for k in range(0, len(args_list)):
        try:
            items.append(q.get_nowait())
        except Exception as e:
            break

    return items


if __name__ == "__main__":

    lst = []
    for target in TARGETS:

        target = target.encode('utf-8').strip()

        if not is_valid_uri(target):
            log2console('**Error: Bad target!')
            continue

        # Create folder with site name inside log folder
        regex = '^(https?|ftps?)://'
        site = re.sub(regex, '', target)

        regex = '^/'
        site = re.sub(regex, '', site)

        site = site.replace('/','_')

        logdir = os.path.join(PATH, LOGPATH, site)
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        logall = os.path.join(logdir, LOGALL)
        logdomains = os.path.join(logdir, LOGDOMAINS)
        logskip = os.path.join(logdir, LOGSKIP)
        logurls = os.path.join(logdir, LOGURLS)
        logerr= os.path.join(logdir, LOGERR)

        deleteContent(logall)
        deleteContent(logdomains)
        deleteContent(logskip)
        deleteContent(logurls)
        deleteContent(logerr)

        writeHeader(logall)
        writeHeader(logdomains)
        writeHeader(logskip)
        writeHeader(logurls)
        writeHeader(logerr)

        root = {
            'time': datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3],
            'status': 0,
            'uri': target.encode('utf-8').strip(),
            'uri_original': target.encode('utf-8').strip(),
            'depth': 0,
            'uuid': uuid.uuid4(),
            'pid': [str(0)],
            'child': [],
            'domain': '',
            'logdir': logdir}

        lst.append(root)

    while lst:

        log2console("*"*100)
        log2console(str(len(lst)))

        pool = ThreadPool(PROC)

        # map only supports calling functions with one argument.
        # For more arguments, use zip(arg1, arg2, ...)
        # In Python 3.3+, use starmap instead.
        lst = pool.map(webscraping, lst)

        pool.close()
        pool.join()

        log2console("-" * 100)
