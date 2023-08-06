import time
from concurrent.futures import ThreadPoolExecutor

from convisoappsec.common.docker import SCSCommon
from transitions import Machine
from transitions.extensions.states import Timeout, add_state_features


RAW_STATE_MSG = 'Scanner {} entered on {} state'


@add_state_features(Timeout)
class ScannerMachine(Machine):
    pass


class ScannerEntity:

    def __init__(self, token, scanner, logger, timeout):
        self.logger = logger
        self.token = token

        self.scanner = self.__setup_scanner(scanner)
        self.name = self.scanner.name
        self.results = None

        self.states = [
            'waiting',
            {'name': 'pulling', 'timeout': timeout, 'on_timeout': self._on_timeout},
            {'name': 'running', 'timeout': timeout, 'on_timeout': self._on_timeout},
            {'name': 'sending', 'timeout': timeout, 'on_timeout': self._on_timeout},
            'done'
        ]
        self.machine = ScannerMachine(
            model=self,
            states=self.states,
            initial='waiting'
        )
        self.machine.add_ordered_transitions()
        self._set_callbacks()
        self.to_waiting()

    def __setup_scanner(self, scanner):
        if isinstance(scanner, SCSCommon):
            return scanner
        else:
            return self._instanciate_scanner(scanner)

    def _set_callbacks(self):
        self.machine.on_enter_waiting('_on_waiting')
        self.machine.on_enter_pulling('_on_pulling')
        self.machine.on_enter_running('_on_running')
        self.machine.on_enter_sending('_on_sending')
        self.machine.on_enter_done('_on_done')

    def _instanciate_scanner(self, data):
        return SCSCommon(
            **data,
            token=self.token,
            logger=self.logger,
        )

    def _on_timeout(self):
        self.logger.debug('Scanner {} timeout on state {}'.format(
            self.name, self.state
        ))

    def _on_waiting(self):
        self.logger.debug(RAW_STATE_MSG.format(
            self.name, self.state
        ))

    def _on_pulling(self):
        self.logger.debug(RAW_STATE_MSG.format(
            self.name, self.state
        ))
        self.logger.info('   Pulling {} image'.format(self.name))
        image = self.scanner.pull()
        if image:
            self.logger.debug('Image: {}'.format(image))
            self.next_state()
        else:
            raise RuntimeError("Image not found.")

    def _on_running(self):
        self.logger.info('   Scanner {} is running.'.format(
            self.scanner.repository_name, self.state
        ))
        self.scanner.run()
        self.end_time = time.time()
        self.logger.debug('Total execution time for {} was {:2f}'.format(
            self.scanner.repository_name,
            self.end_time - self.start_time
        ))
        status_code = self.scanner.wait()
        self.logger.info('   Scanner {}@{} returned status code {}'.format(
            self.scanner.repository_name,
            self.name,
            status_code
        ))
        self.next_state()

    def _on_sending(self):
        self.logger.debug(RAW_STATE_MSG.format(
            self.name, self.state
        ))
        self.results = self.scanner.get_container_reports()
        self.next_state()

    def _on_done(self):
        self.logger.debug(RAW_STATE_MSG.format(
            self.scanner.repository_name, self.state
        ))
        self.scanner.container.remove(v=True, force=True)

    def start(self):
        self.start_time = time.time()
        self.to_pulling()


class ContainerWrapper:

    def __init__(self, token, containers_map, logger, timeout, max_workers=5):
        self.token = token
        self.logger = logger
        self.max_workers = max_workers
        self.scanners = [
            ScannerEntity(
                token=token,
                scanner=scanner,
                logger=logger,
                timeout=timeout
            )
            for scanner in containers_map.values()
        ]

    def run(self):
        self.logger.debug("Starting Execution")
        with ThreadPoolExecutor(max_workers=self.max_workers) as exeggutor:
            for scanner in self.scanners:
                exeggutor.submit(scanner.start)
