import serial
from serial.tools.list_ports import comports

from pymodaq_plugins_piezosystemjena.hardware.Serial_NV403CLE import NV403CLE

from pymodaq.daq_move.utility_classes import DAQ_Move_base  # base class
from pymodaq.daq_move.utility_classes import comon_parameters, comon_parameters_fun # common set of parameters for all actuators
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo  # object used to send info back to the main thread
from easydict import EasyDict as edict  # type of dict

class DAQ_Move_nv403cle(DAQ_Move_base):
    """
        Plugin using pyserial to control an NV403CLE stage controller
        from Piezosystem Jena.

        Support USB connection (No RS232 provided)

        Only supports closed loop operation

        =============== ==============
        **Attributes**    **Type**
        *params*          dictionnary
        =============== ==============
    """

    _dvc = comports()
    com = [d.device for d in _dvc if d.description.startswith('piezojena NV40/3CL USB')]

    _controller_units = 'um'
    is_multiaxes = True
    stage_names = ['X', 'Y', 'Z']
    min_bound = 0.0  #*µm
    max_bound = 79.0 #µm

    params = [{'title': 'Controller ID:', 'name': 'controller_id', 'type': 'str', 'value': '', 'readonly': True},
              {'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'values': com},
              {'title': 'Display Brightness', 'name': 'display_brightness', 'type': 'int',
               'value': 255, 'limits':[0,255], 'default': 255},
              {'title': 'Remote', 'name': 'remote', 'type': 'bool', 'value': False},
              {'title': 'Home Position', 'name': 'home_position', 'type': 'float', 'value': 0.0,
               'limits': [min_bound,max_bound]},
              {'title': 'Measure Offset', 'name': 'measure_offset', 'type': 'bool_push', 'value': False},
              {'title': 'MultiAxes:', 'name': 'multiaxes', 'type': 'group', 'visible': is_multiaxes, 'children':[
                  {'title': 'is Multiaxes:', 'name': 'ismultiaxes', 'type': 'bool', 'value': is_multiaxes,
                   'default': False},
                  {'title': 'Status:', 'name': 'multi_status', 'type': 'list', 'value': 'Master',
                   'limits': ['Master', 'Slave']},
                  {'title': 'Axis:', 'name': 'axis', 'type': 'list', 'limits': stage_names},
                  ]
              }
             ] + comon_parameters


    def __init__(self, parent=None, params_state=None):
        """
            Initialize the the class

            ============== ================================================ ==========================================================================================
            **Parameters**  **Type**                                         **Description**

            *parent*        Caller object of this plugin                    see DAQ_Move_main.DAQ_Move_stage
            *params_state*  list of dicts                                   saved state of the plugins parameters list
            ============== ================================================ ==========================================================================================

        """
        super().__init__(parent, params_state)

        self.settings.child('epsilon').setValue(0.1)
        self.settings.child('timeout').setValue(1.0)

        self.settings.child('bounds', 'is_bounds').setValue(True)
        self.settings.child('bounds', 'is_bounds').setReadonly()

        self.settings.child('bounds', 'max_bound').setValue(self.max_bound)
        self.settings.child('bounds', 'max_bound').setReadonly()

        self.settings.child('bounds', 'min_bound').setValue(self.min_bound)
        self.settings.child('bounds', 'min_bound').setReadonly()

        #Disabling the scaling
        self.settings.child('scaling', 'use_scaling').setValue(True)
        self.settings.child('scaling', 'use_scaling').setReadonly()
        self.settings.child('scaling', 'scaling').setValue(1.0)
        self.settings.child('scaling', 'scaling').setReadonly()
        self.settings.child('scaling', 'offset').setValue(0.0)
        self.settings.child('scaling', 'offset').setReadonly()

    def get_current_axis_index(self) -> int:
        return self.stage_names.index(self.settings.child('multiaxes', 'axis').value())

    def check_position(self):
        """
            Get the current position from the hardware with scaling conversion.

            Returns
            -------
            float
                The position obtained after scaling conversion.

            See Also
            --------
            DAQ_Move_base.get_position_with_scaling, daq_utils.ThreadCommand
        """
        #Get the index of the current axis
        ax_idx = self.get_current_axis_index()
        #Get Position
        pos = self.controller.get_position(ax_idx)
        pos = self.get_position_with_scaling(pos)

        self.emit_status(ThreadCommand('check_position', [round(pos,4)]))
        return pos

    def close(self):
        """
          Close communication with the Serial Port.
        """
        #Reset light to 255
        self.controller.set_display_brightness(255)
        axid = self.get_current_axis_index()
        self.controller.set_axis_remote(axis_index=axid, remote=False)

        #Give the controller the close signal
        self.controller.close()

    def commit_settings(self, param):
        """
            | Activate any parameter changes on the PI_GCS2 hardware.
            |
            | Called after a param_tree_changed signal from DAQ_Move_main.
        """
        if param.name() == 'display_brightness':
            self.controller.set_display_brightness(brightness=param.value())
            self.emit_status(ThreadCommand('Update_Status',
                                           [f'Set display brightness : {param.value()}']))
        elif param.name() == 'remote':
            ax_idx = self.get_current_axis_index()
            self.controller.set_axis_remote(axis_index=ax_idx,remote=param.value())
            self.emit_status(ThreadCommand('Update_Status',
                                           [f'Axis {ax_idx} - {self.stage_names[ax_idx]} set to remote = {param.value()}']))
        elif param.name() == 'measure_offset':
            if param.value() == True:
                ax_idx = self.get_current_axis_index()
                offset = self.controller.get_position_offset(axis_index=ax_idx)
                self.settings.child('scaling', 'offset').setValue(offset)
                self.emit_status(ThreadCommand('Update_Status',
                                           [f'Axis {ax_idx} - {self.stage_names[ax_idx]}:'
                                            f'measured offset = {offset:.3f}']))
                self.settings.child('measure_offset').setValue(False)
            else:
                pass


    def ini_stage(self, controller=None):
        """
            Initialize the controller and stages (axes) with given parameters.

            ============== ================================================ ==========================================================================================
            **Parameters**  **Type**                                         **Description**

            *controller*    instance of the specific controller object       If defined this hardware will use it and will not initialize its own controller instance
            ============== ================================================ ==========================================================================================

            Returns
            -------
            Easydict
                dictionnary containing keys:
                 * *info* : string displaying various info
                 * *controller*: instance of the controller object in order to control other axes without the need to init the same controller twice
                 * *stage*: instance of the stage (axis or whatever) object
                 * *initialized*: boolean indicating if initialization has been done corretly

            See Also
            --------
             daq_utils.ThreadCommand
        """
        try:
            # initialize the stage and its controller status
            # controller is an object that may be passed to other instances of DAQ_Move_Mock in case
            # of one controller controlling multiaxes

            self.status.update(edict(info="", controller=None, initialized=False))

            # check whether this stage is controlled by a multiaxe controller (to be defined for each plugin)

            # if multiaxes then init the controller here if Master state otherwise use external controller
            if self.settings.child('multiaxes', 'ismultiaxes').value() and \
                    self.settings.child('multiaxes', 'multi_status').value() == "Slave":
                if controller is None:
                    raise Exception('no controller has been defined externally while this axe is a slave one')
                else:
                    self.controller = controller
            else:  # Master stage
                #Read COM port from params and create the controller object
                com = self.settings.child('com_port').value()
                self.controller = NV403CLE(com)

                #Open the controller
                self.controller.open()

            #Make sure the controller axis is closed_loop & remote
            axid = self.get_current_axis_index()
            self.controller.set_axis_remote(axis_index=axid, remote=True)
            self.settings.child('remote').setValue(True)
            self.controller.set_closed_loop(axis_index=axid, closed=True)


            #Measure the axis offset and put it as calibration parameter
            offset = self.controller.get_position_offset(axis_index=axid)
            self.settings.child('scaling', 'offset').setValue(offset)
            self.emit_status(ThreadCommand('Update_Status',
                                           [f'Axis {axid} - {self.stage_names[axid]}:'
                                            f'measured offset = {offset:.3f}']))

            #Look at the com devices and search the device description
            controller_id = self.controller.get_infos()

            self.settings.child('controller_id').setValue(controller_id)
            self.status.info = controller_id
            self.status.controller = self.controller
            self.status.initialized = True

            return self.status


        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [getLineInfo() + str(e), 'log']))
            self.status.info = getLineInfo() + str(e)
            self.status.initialized = False
            return self.status

    def move_Abs(self, position):
        """
            Make the absolute move from the given position after thread command signal was received in DAQ_Move_main.

            =============== ========= =======================
            **Parameters**  **Type**   **Description**

            *position*       float     The absolute position
            =============== ========= =======================

            See Also
            --------
            DAQ_Move_base.set_position_with_scaling, DAQ_Move_base.poll_moving

        """
        #Restrict target position to the bounds
        position = self.check_bound(position)
        ax_id = self.get_current_axis_index()

        self.target_position = position
        self.controller.set_position(axis_index=ax_id, value=position)

        self.poll_moving()

    def move_Rel(self, position):
        """
            Make the relative move from the given position after thread command signal was received in DAQ_Move_main.

            =============== ========= =======================
            **Parameters**  **Type**   **Description**

            *position*       float     The absolute position
            =============== ========= =======================

            See Also
            --------
            hardware.set_position_with_scaling, DAQ_Move_base.poll_moving

        """
        #Restrict the relative move to the bonds
        position = self.check_bound(self.current_position + position) - self.current_position

        #Setup the stuff
        ax_id = self.get_current_axis_index()
        abs_mov = position + self.current_position

        self.controller.set_position(axis_index=ax_id, value=abs_mov)

        self.target_position = abs_mov
        self.poll_moving()

    def move_Home(self):
        """
          Send the update status thread command.
            See Also
            --------
            daq_utils.ThreadCommand
        """
        homepos = self.settings.child('home_position').value()
        self.move_Abs(homepos)

        self.emit_status(ThreadCommand('Update_Status', ['Homing']))

    def stop_motion(self):
        """
          Call the specific move_done function (depending on the hardware).

          See Also
          --------
          move_done
        """
        self.move_done()