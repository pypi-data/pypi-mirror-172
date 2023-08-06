import abc


class Command(abc.ABC):
    @property
    @abc.abstractmethod
    def s_target(self):
        pass

    @classmethod
    @abc.abstractmethod
    def apply(self, cell_text, command_list, verbose=False):
        """ applies command to cell text

        Args:
            cell_text (str): text of a jupyter cell
            command_list (list): tuple of (s_cmd, idx) where s_cmd is a command
                containing self.s_command and idx is the location in cell_text
                it was originally found (see search_command())
            verbose (bool): toggles command line output

        Returns:
            cell_text (str): text of jupyter cell (after command applied)
        """
        pass


class RemoveCell(Command):
    s_target = 'rm'

    @classmethod
    def apply(self, cell_text, command_list, verbose=False):
        return None


class ClearCell(Command):
    s_target = 'clear'

    @classmethod
    def apply(self, cell_text, command_list, verbose=False):
        return ''


class SnipCell(Command):
    """ removes all text between snip-start and snip-end"""
    s_target = 'snip'
    s_start = 'snip-start'
    s_end = 'snip-end'
    VERBOSE_MAX = 30

    @classmethod
    def apply(cls, cell_text, command_list, verbose=False):
        """

        >>> index_hlp = '0123456789'
        >>> cell_text = '00!!!00!!!'
        >>> command_list = [(SnipCell.s_start,  2),
        ...                 (SnipCell.s_end, 5),
        ...                 (SnipCell.s_start, 7),
        ...                 (SnipCell.s_end, 10)]
        >>> SnipCell.apply(cell_text, command_list)
        '0000'
        >>> SnipCell.apply(cell_text, command_list, verbose=True)
        snipping: !!!
        snipping: !!!
        '0000'

        Args:
            cell_text (str): text of jupyter cell (all commands removed)
            command_list (list): list of (cmd_text, idx) tuples.  cmd_text are
                observed commands and idx refers to their found location in
                cell_text
            verbose (bool): toggles command line output

        Returns:
            cell_text (str): text of jupyter cell, now snipped
        """

        for cmd, _ in command_list:
            assert cmd in (cls.s_start, cls.s_end), 'invalid snip command'

        s_error = 'malformed snip sequence (start, end, start, end, ...)'
        for (cmd0, idx0), (cmd1, idx1) in zip(command_list[:-1][::-2],
                                              command_list[::-2]):
            assert cmd0 == cls.s_start, s_error
            assert cmd1 == cls.s_end, s_error

            if verbose:
                print(f'snipping: {cell_text[idx0: idx1][:cls.VERBOSE_MAX]}')

            # snip
            cell_text = cell_text[:idx0] + cell_text[idx1:]

        return cell_text


all_command = RemoveCell, ClearCell, SnipCell
