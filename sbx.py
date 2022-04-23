from ic.node import Node


def main():
    n = Node(1)
    print(n.signal)


def update_signal(self):
    if self.signal.is_locked():
        return self.signal.value
    if not self._settings['inputs']:
        return self.signal.value
    if not self.inputs.check():
        raise RuntimeError('Not connected!')
    for node in self.inputs:
        node.update_signal()
        if node.signal.value > self.signal.value:
            self.signal.set(node.signal.value)
    return self.signal.value


if __name__ == '__main__':
    main()
